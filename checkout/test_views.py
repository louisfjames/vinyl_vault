from decimal import Decimal
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse
from albums.models import Album
from checkout.models import Order


class CheckoutViewsTestCase(TestCase):
    """
    Tests for the checkout app's views: checkout, payment, and
    checkout_success. Stripe's PaymentIntent.create is mocked throughout
    to avoid real network calls during testing.
    """

    def setUp(self):
        self.album = Album.objects.create(
            title='Test Album',
            artist='Test Artist',
            price=Decimal('19.99'),
        )
        self.valid_form_data = {
            'full_name': 'Test Customer',
            'email': 'testcustomer@example.com',
            'phone_number': '01234567890',
            'country': 'GB',
            'postcode': 'SN14 0FZ',
            'town_or_city': 'Chippenham',
            'street_address1': '1 Test Street',
            'street_address2': '',
            'county': 'Wiltshire',
        }

    def _add_album_to_session_bag(self):
        session = self.client.session
        session['bag'] = {str(self.album.id): 1}
        session.save()

    # --- checkout view ---

    def test_checkout_redirects_on_empty_bag(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('albums:browse_albums'))

    def test_checkout_get_renders_form_with_items_in_bag(self):
        self._add_album_to_session_bag()
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Album')

    def test_checkout_post_valid_data_redirects_to_payment(self):
        self._add_album_to_session_bag()
        response = self.client.post(reverse('checkout'), self.valid_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('payment'))
        self.assertIn('checkout_data', self.client.session)

    def test_checkout_post_invalid_data_shows_error(self):
        self._add_album_to_session_bag()
        incomplete_data = self.valid_form_data.copy()
        incomplete_data['full_name'] = ''
        response = self.client.post(reverse('checkout'), incomplete_data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('checkout_data', self.client.session)

    # --- payment view ---

    def test_payment_redirects_without_checkout_data(self):
        self._add_album_to_session_bag()
        response = self.client.get(reverse('payment'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('checkout'))

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_payment_get_loads_with_mocked_stripe_intent(self, mock_create):
        mock_create.return_value = MagicMock(client_secret='test_client_secret')

        self._add_album_to_session_bag()
        session = self.client.session
        session['checkout_data'] = self.valid_form_data
        session.save()

        response = self.client.get(reverse('payment'))
        self.assertEqual(response.status_code, 200)
        mock_create.assert_called_once()

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_payment_post_valid_creates_order_and_redirects(self, mock_create):
        mock_create.return_value = MagicMock(client_secret='test_client_secret')

        self._add_album_to_session_bag()
        session = self.client.session
        session['checkout_data'] = self.valid_form_data
        session.save()

        response = self.client.post(reverse('payment'), self.valid_form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.email, 'testcustomer@example.com')
        # session should be cleared after a successful order
        self.assertNotIn('checkout_data', self.client.session)
        self.assertNotIn('bag', self.client.session)

    # --- checkout_success view ---

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_success_loads_for_valid_order(self, mock_create):
        mock_create.return_value = MagicMock(client_secret='test_client_secret')

        self._add_album_to_session_bag()
        session = self.client.session
        session['checkout_data'] = self.valid_form_data
        session.save()
        self.client.post(reverse('payment'), self.valid_form_data)

        order = Order.objects.first()
        response = self.client.get(
            reverse('checkout_success', args=[order.order_number])
        )
        self.assertEqual(response.status_code, 200)

    def test_checkout_success_404_for_invalid_order_number(self):
        response = self.client.get(
            reverse('checkout_success', args=['nonexistent123'])
        )
        self.assertEqual(response.status_code, 404)
