from django.shortcuts import render, redirect, reverse
from django.contrib import messages
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
