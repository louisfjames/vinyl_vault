from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from albums.models import Album

# Create your views here.

def view_bag(request):
    """ A view to renders the bag contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    Add a specified quantity of an album to the shopping bag.

    Reads the target album's quantity and a redirect URL from the
    POST data. If the album is already in the bag, its quantity is
    incremented; otherwise a new entry is created. The updated bag
    is saved back to the session, and the user is redirected to
    the given URL with a success message.
    """
    album = get_object_or_404(Album, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in bag:
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    messages.success(request, f'Added {album.title} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)