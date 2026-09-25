from django.conf import settings
from albums.models import Album

def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        album = Album.objects.get(pk=item_id)
        price = album.sale_price if album.sale_price else album.price
        subtotal = price * quantity
        total += subtotal
        product_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'album': album,
            'price': price,
            'subtotal': subtotal,
        })

    delivery = settings.STANDARD_DELIVERY_COST
    grand_total = total + delivery

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
