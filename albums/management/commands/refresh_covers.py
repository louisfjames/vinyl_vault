from django.core.management.base import BaseCommand
from albums.albums.deezer import get_album
from albums.models import Album


class Command(BaseCommand):
    """
    One-off management command to refresh cover_image_url for existing
    albums using Deezer's higher-resolution cover_xl image, since covers
    seeded via cover_medium appeared blurry once displayed at larger sizes
    on the album detail page.

    Only touches cover_image_url - leaves every other field (price, stock,
    format, etc.) untouched.

    Usage:
        python manage.py refresh_covers
    """
    def handle(self, *args, **kwargs):
        updated_count = 0
        skipped_count = 0

        for album in Album.objects.exclude(deezer_id__isnull=True):
            details = get_album(album.deezer_id)
            if not details:
                self.stdout.write(self.style.WARNING(
                    f"Could not fetch deezer_id {album.deezer_id} ({album.title})"
                ))
                skipped_count += 1
                continue

            new_cover = details.get('cover_xl')
            if new_cover:
                album.cover_image_url = new_cover
                album.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated cover: {album.title}"))
            else:
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. Updated {updated_count}, skipped {skipped_count}."
        ))
