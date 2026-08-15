from django.urls import path
from . import views

app_name = 'albums'

urlpatterns = [
    path('<int:album_id>/', views.album_detail, name='album_detail'),
    path('', views.browse_albums, name='browse_albums'),
    path('sale/', views.sale_albums, name='sale_albums'),
    path('new-releases/', views.new_releases, name='new_releases'),
    path('search/', views.album_search, name='album_search'),
]
