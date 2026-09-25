from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
import json

from bag.contexts import bag_contents
from .forms import OrderForm
from .models import Order, OrderLineItem
from albums.models import Album
from profiles.models import UserProfile

import stripe


def checkout(request):
    """
    Collect the customer's delivery and contact details, then move on
    to the payment step once the form is valid.
    """
    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            request.session['checkout_data'] = order_form.cleaned_data
            return redirect(reverse('payment'))
        else:
            messages.error(request, 'There was an error with your form. '
                                     'Please double check your information.')
    else:
        order_form = OrderForm()

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is currently empty")
        return redirect(reverse('albums:browse_albums'))

    current_bag = bag_contents(request)
    bag_items = current_bag['bag_items']
    total = current_bag['total']
    delivery = settings.STANDARD_DELIVERY_COST
    grand_total = total + delivery

    context = {
        'order_form': order_form,
        'bag_items': bag_items,
        'total': total,
        'delivery': delivery,
        'grand_total': grand_total,
    }
    return render(request, 'checkout/checkout.html', context)


def payment(request):
    """
    Create a Stripe PaymentIntent and render the card payment form.
    On POST (after the card has been confirmed client-side), create
    the Order and OrderLineItems from the session data and bag, then
    redirect to the success page.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    checkout_data = request.session.get('checkout_data')
    if not checkout_data:
        messages.error(request, "Please enter your details before payment.")
        return redirect(reverse('checkout'))

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is currently empty")
        return redirect(reverse('albums:browse_albums'))

    if request.method == 'POST':
        order_form = OrderForm(checkout_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.original_bag = json.dumps(bag)

            if request.user.is_authenticated:
                profile = UserProfile.objects.get(user=request.user)
                order.user_profile = profile

            order.save()
            for item_id, quantity in bag.items():
                try:
                    album = Album.objects.get(id=item_id)
                    OrderLineItem.objects.create(
                        order=order,
                        album=album,
                        quantity=quantity,
                    )
                except Album.DoesNotExist:
                    messages.error(request, (
                        "One of the albums in your bag wasn't found in "
                        "our database. Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('bag:view_bag'))

            # Send confirmation email
            customer_email = order.email
            subject = render_to_string(
                'checkout/confirmation_email_subject.txt',
                {'order': order})
            body = render_to_string(
                'checkout/confirmation_email_body.txt',
                {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [customer_email]
            )

            del request.session['checkout_data']
            if 'bag' in request.session:
                del request.session['bag']
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error placing your order. '
                                     'Please try again.')
            return redirect(reverse('checkout'))

    current_bag = bag_contents(request)
    bag_items = current_bag['bag_items']
    total = current_bag['total']
    delivery = settings.STANDARD_DELIVERY_COST
    grand_total = total + delivery
    stripe_total = round(grand_total * 100)

    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    context = {
        'bag_items': bag_items,
        'total': total,
        'delivery': delivery,
        'grand_total': grand_total,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, 'checkout/payment.html', context)


def checkout_success(request, order_number):
    """
    Display the order confirmation page for a completed checkout.

    Looks up the Order by its order_number (passed in the URL after
    payment succeeds and the Order is created), clears the session
    bag, and renders the confirmation with the order's details.
    """
    order = get_object_or_404(Order, order_number=order_number)
    order_items = order.lineitems.all()
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    context = {
        'order': order,
        'order_items': order_items,
    }

    return render(request, 'checkout/checkout_success.html', context)