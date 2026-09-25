from django import forms
from .models import Album


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = [
            'title', 'artist', 'price', 'sale_price', 'is_on_sale',
            'release_date', 'genre', 'cover_image_url', 'description',
            'format', 'colour_variant', 'label', 'stock_quantity',
            'tracklist', 'deezer_id', 'is_featured', 'featured_reason',
        ]
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'tracklist': forms.Textarea(attrs={'rows': 6}),
            'featured_reason': forms.Textarea(attrs={'rows': 2}),
        }
