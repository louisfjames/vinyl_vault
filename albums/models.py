from django.db import models

class Album(models.Model):
    FORMAT_CHOICES = [
        ('vinyl', 'Standard Vinyl'),
        ('special_edition', 'Special Edition'),
        ('coloured_vinyl', 'Coloured Vinyl'),
    ]

    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    is_on_sale = models.BooleanField(default=False)
    release_date = models.DateField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True)
    cover_image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='vinyl')
    colour_variant = models.CharField(max_length=100, blank=True)
    label = models.CharField(max_length=200, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    tracklist = models.TextField(blank=True)
    deezer_id = models.IntegerField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} — {self.artist}"
