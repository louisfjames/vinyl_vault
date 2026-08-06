from django.shortcuts import render
from albums.models import Album

# Create your views here.

def index(request):
    """ A view that returns the index page """
    album_data = Album.objects.all().order_by('-release_date')

    context = {
           'latest_releases': album_data[:5],
           'featured_album': album_data.first(),
           'sale_items': album_data.filter(is_on_sale=True)[:4],
       }
    return render(request, 'core/index.html', context)
