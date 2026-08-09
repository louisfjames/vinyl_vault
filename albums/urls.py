from django.urls import path
from . import views

app_name = 'albums'

urlpatterns = [
    path('<int:album_id>/', views.album_detail, name='album_detail'),
    path('', views.browse_albums, name='browse_albums'),
]
