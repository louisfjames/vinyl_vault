from django.urls import path
from . import views

app_name = 'albums'

urlpatterns = [
    path('<int:album_id>/', views.album_detail, name='album_detail'),
    path('', views.browse_albums, name='browse_albums'),
    path('sale/', views.sale_albums, name='sale_albums'),
    path('new-releases/', views.new_releases, name='new_releases'),
    path('search/', views.album_search, name='album_search'),
    path('store-management/', views.store_management, name='store_management'),
    path('add/', views.add_album, name='add_album'),
    path('delete/<int:album_id>/', views.delete_album, name='delete_album'),
    path('edit/<int:album_id>/', views.edit_album, name='edit_album'),
]
