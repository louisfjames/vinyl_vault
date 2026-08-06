from django.core.management.base import BaseCommand
from albums.data.albums import albums
from albums.albums.deezer import get_album
from albums.models import Album


class Command(BaseCommand):
    """
    Management command to seed the Album database from a curated list of
    Deezer album IDs (albums/data/albums.py).

    For each entry in the curated list, fetches full album details from the
    Deezer API (via albums.deezer.get_album), then creates a corresponding
    Album row in the database - mapping title, artist, genre, cover image,
    label, release date, and tracklist from the API response.

    Store-specific fields Deezer has no concept of (price, stock_quantity,
    format, colour_variant, is_on_sale) are left as defaults and must be
    filled in manually afterwards, e.g. via Django admin.

    Safe to re-run: entries whose deezer_id already exists in the database
    are skipped rather than duplicated.

    Usage:
        python manage.py seed_albums
    """

    def handle(self, *args, **kwargs):
        created_count = 0
        skipped_count = 0

        for entry in albums:
            deezer_id = entry['deezer_id']

            if Album.objects.filter(deezer_id=deezer_id).exists():
                skipped_count += 1
                continue

            details = get_album(deezer_id)
            if not details:
                self.stdout.write(self.style.WARNING(
                    f"Could not fetch deezer_id {deezer_id} ({entry.get('artist')} - {entry.get('album')})"
                ))
                continue

            genres = details.get('genres', {}).get('data', [])
            genre = genres[0]['name'] if genres else ''

            tracks = details.get('tracks', {}).get('data', [])
            tracklist = '\n'.join(t['title'] for t in tracks)

            Album.objects.create(
                title=details.get('title', ''),
                artist=details.get('artist', {}).get('name', ''),
                price=0,  # placeholder and will update manually afterwards
                release_date=details.get('release_date') or None,
                genre=genre,
                cover_image_url=details.get('cover_medium', ''),
                label=details.get('label', ''),
                tracklist=tracklist,
                deezer_id=deezer_id,
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"Created: {details.get('title')}"))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. Created {created_count}, skipped {skipped_count} already-existing."
        ))
        