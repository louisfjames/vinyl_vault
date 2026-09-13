from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
import json

from bag.contexts import bag_contents
from .forms import OrderForm
from .models import Order, OrderLineItem
from albums.models import Album


def checkout(request):
    bag = request.session.get('bag', {})

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
            order = order_form.save(commit=False)
            order.original_bag = json.dumps(bag)
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

            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. '
                                     'Please double check your information.')

    if not bag:
        messages.error(request, "Your bag is currently empty")
        return redirect(reverse('albums'))

    current_bag = bag_contents(request)
    bag_items = current_bag['bag_items']
    total = current_bag['total']
    delivery = settings.STANDARD_DELIVERY_COST
    grand_total = total + delivery

    if request.method != 'POST':
        order_form = OrderForm()

    context = {
        'order_form': order_form,
        'bag_items': bag_items,
        'total': total,
        'delivery': delivery,
        'grand_total': grand_total,
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)
