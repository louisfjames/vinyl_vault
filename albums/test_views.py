from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from albums.models import Album


class AlbumsViewsTestCase(TestCase):
    """
    Tests for the albums app's views, focused on two areas: permission
    boundaries around the superuser-only Store Management actions, and
    safe fallback behaviour on the public-facing views.
    """

    def setUp(self):
        self.regular_user = User.objects.create_user(
            username='regularuser', password='testpass123'
        )
        self.superuser = User.objects.create_superuser(
            username='adminuser', password='testpass123',
            email='admin@example.com'
        )
        self.album = Album.objects.create(
            title='Test Album',
            artist='Test Artist',
            price=Decimal('19.99'),
        )

    # --- Public-facing views ---

    def test_album_detail_returns_404_for_invalid_id(self):
        response = self.client.get(reverse('albums:album_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_album_detail_loads_successfully_for_valid_id(self):
        response = self.client.get(
            reverse('albums:album_detail', args=[self.album.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Album')

    def test_browse_albums_falls_back_on_invalid_page_number(self):
        response = self.client.get(
            reverse('albums:browse_albums'), {'page': 'not-a-number'}
        )
        self.assertEqual(response.status_code, 200)

    # --- Store Management: permission boundaries ---

    def test_store_management_views_reject_anonymous_users(self):
        """
        All four superuser-only views should redirect an anonymous
        (not logged in) visitor rather than showing the page.
        """
        protected_urls = [
            reverse('albums:store_management'),
            reverse('albums:add_album'),
            reverse('albums:edit_album', args=[self.album.id]),
        ]
        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)

    def test_store_management_views_reject_regular_users(self):
        """
        All four superuser-only views should redirect a logged-in but
        non-superuser user rather than showing the page.
        """
        self.client.login(username='regularuser', password='testpass123')
        protected_urls = [
            reverse('albums:store_management'),
            reverse('albums:add_album'),
            reverse('albums:edit_album', args=[self.album.id]),
        ]
        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)

        response = self.client.post(
            reverse('albums:delete_album', args=[self.album.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Album.objects.filter(id=self.album.id).exists())

    # --- Store Management: superuser access ---

    def test_store_management_views_load_for_superuser(self):
        self.client.login(username='adminuser', password='testpass123')
        response = self.client.get(reverse('albums:store_management'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Album')

        response = self.client.get(reverse('albums:add_album'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse('albums:edit_album', args=[self.album.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_album_removes_album_for_superuser(self):
        self.client.login(username='adminuser', password='testpass123')
        response = self.client.post(
            reverse('albums:delete_album', args=[self.album.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Album.objects.filter(id=self.album.id).exists())

    # --- Delete album: method restriction ---

    def test_delete_album_rejects_get_request(self):
        self.client.login(username='adminuser', password='testpass123')
        response = self.client.get(
            reverse('albums:delete_album', args=[self.album.id])
        )
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Album.objects.filter(id=self.album.id).exists())
