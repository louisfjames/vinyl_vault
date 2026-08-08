from django.shortcuts import render, get_object_or_404
from .models import Album

def album_detail(request, album_id):
    """
    Display a single album's detail page.

    Looks up the Album matching album_id (from the URL, e.g. /albums/53/)
    and renders its full details - cover, title, artist, price,
    and add-to-basket action.

    Defensive design: uses get_object_or_404 rather than Album.objects.get,
    so an invalid or non-existent album_id (e.g. a bad link, a deleted
    album, or someone manually editing the URL) results in a clean 404
    page instead of an unhandled DoesNotExist exception crashing the view.
    """

    album = get_object_or_404(Album, pk=album_id)

    context = {
        'album': album,
    }
    return render(request, 'albums/album_detail.html', context)
