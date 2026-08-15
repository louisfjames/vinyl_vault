from django.shortcuts import render, get_object_or_404
from .models import Album
from django.core.paginator import Paginator
from datetime import date, timedelta

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
    invalid/missing 'page' query param falls back instead
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


def sale_albums(request):
    """
    Display a paginated grid of albums currently on sale (16 per page,
    4x4 grid), ordered by title. Uses get_page() so an invalid/missing
    'page' query param falls back instead of erroring.
    """
    album_list = Album.objects.filter(is_on_sale=True).order_by('title')
    paginator = Paginator(album_list, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'albums/sale.html', context)


def new_releases(request):
    """
    Display a paginated grid of albums released within the last year
    (16 per page, 4x4 grid), ordered by most recent release_date first.
    Uses get_page() so an invalid/missing 'page' query param falls back
    instead of erroring.
    """
    one_year_ago = date.today() - timedelta(days=365)
    album_list = Album.objects.filter(
        release_date__gte=one_year_ago
    ).order_by('-release_date')

    paginator = Paginator(album_list, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'albums/new_releases.html', context)


def album_search(request):
    """
    Render a paginated grid of albums matching a search query.

    Retrieves the 'q' parameter from the request and filters Album
    records by title using a case‑insensitive containment match.
    The filtered queryset is ordered alphabetically and paginated
    into 16‑item pages to maintain the same 4×4 layout used on the
    main browse view. Uses get_page() to safely handle invalid or
    missing 'page' parameters.
    """
    query = request.GET.get('q', '')

    album_list = Album.objects.filter(title__icontains=query).order_by('title')

    paginator = Paginator(album_list, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'albums/search_results.html', context)
