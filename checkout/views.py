from django.shortcuts import render
from bag.contexts import bag_contents
from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is currently empty")
        return redirect(reverse('albums'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    order_form = OrderForm()

    context = {
        'order_form': order_form,
        'total': total,
    }
    return render(request, 'checkout/checkout.html', context)
