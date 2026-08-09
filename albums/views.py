from django.shortcuts import render, get_object_or_404
from .models import Album
from django.core.paginator import Paginator

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


def browse_albums(request):
    """
    Display a paginated grid of all albums (16 per page, 4x4 grid),
    ordered alphabetically by title. Uses get_page() so an
    invalid/missing 'page' query param falls back gracefully instead
    of erroring.
    """
    album_list = Album.objects.all().order_by('title')
    paginator = Paginator(album_list, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'albums/browse.html', context)
