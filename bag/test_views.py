from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from albums.models import Album


class BagViewsTestCase(TestCase):
    """
    Tests for the bag app's session-based views: view_bag, add_to_bag,
    update_bag, and remove_from_bag. Since the bag has no database model
    of its own, these tests inspect self.client.session directly to
    confirm the session dictionary is being read/written correctly.
    """

    def setUp(self):
        self.album = Album.objects.create(
            title='Test Album',
            artist='Test Artist',
            price=Decimal('19.99'),
        )

    def test_view_bag_loads_successfully(self):
        response = self.client.get(reverse('bag:view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')

    def test_add_to_bag_creates_new_entry(self):
        response = self.client.post(
            reverse('bag:add_to_bag', args=[self.album.id]),
            {'quantity': 2, 'redirect_url': reverse('bag:view_bag')}
        )
        bag = self.client.session['bag']
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(self.album.id), bag)
        self.assertEqual(bag[str(self.album.id)], 2)

    def test_add_to_bag_increments_existing_entry(self):
        self.client.post(
            reverse('bag:add_to_bag', args=[self.album.id]),
            {'quantity': 2, 'redirect_url': reverse('bag:view_bag')}
        )
        self.client.post(
            reverse('bag:add_to_bag', args=[self.album.id]),
            {'quantity': 3, 'redirect_url': reverse('bag:view_bag')}
        )
        bag = self.client.session['bag']
        self.assertEqual(bag[str(self.album.id)], 5)

    def test_update_bag_sets_exact_quantity(self):
        self.client.post(
            reverse('bag:add_to_bag', args=[self.album.id]),
            {'quantity': 2, 'redirect_url': reverse('bag:view_bag')}
        )
        self.client.post(
            reverse('bag:update_bag', args=[self.album.id]),
            {'quantity': 7}
        )
        bag = self.client.session['bag']
        self.assertEqual(bag[str(self.album.id)], 7)

    def test_update_bag_zero_quantity_removes_item(self):
        self.client.post(
            reverse('bag:add_to_bag', args=[self.album.id]),
            {'quantity': 2, 'redirect_url': reverse('bag:view_bag')}
        )
        self.client.post(
            reverse('bag:update_bag', args=[self.album.id]),
            {'quantity': 0}
        )
        bag = self.client.session['bag']
        self.assertNotIn(str(self.album.id), bag)

    def test_remove_from_bag_removes_existing_item(self):
        self.client.post(
            reverse('bag:add_to_bag', args=[self.album.id]),
            {'quantity': 2, 'redirect_url': reverse('bag:view_bag')}
        )
        response = self.client.get(
            reverse('bag:remove_from_bag', args=[self.album.id])
        )
        bag = self.client.session['bag']
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(str(self.album.id), bag)

    def test_remove_from_bag_handles_missing_item_gracefully(self):
        """
        Removing an item that was never added (or already removed)
        should not raise a server error - the view's try/except should
        redirect back to the bag with an error message instead.
        """
        response = self.client.get(
            reverse('bag:remove_from_bag', args=[self.album.id])
        )
        self.assertEqual(response.status_code, 302)
