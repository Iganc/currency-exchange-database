from django.test import TestCase
from django.urls import reverse
from .models import Currency, ExchangeRate


class CurrencyApiTestCase(TestCase):
    def setUp(self):
        # Create Currency objects for USD and EUR
        self.usd = Currency.objects.create(code='USD')
        self.eur = Currency.objects.create(code='EUR')

        # Create an exchange rate for USD to EUR
        ExchangeRate.objects.create(currency_from=self.usd, currency_to=self.eur, exchange_rate=1.1)

    def test_currency_list_view(self):
        response = self.client.get(reverse('currency_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        currencies = [currency['code'] for currency in response.json()]
        self.assertTrue('USD' in currencies)
        self.assertTrue('EUR' in currencies)

    def test_currency_pair_view(self):
        response = self.client.get(
            reverse('currency_exchange_rate', kwargs={'currency_from': 'USD', 'currency_to': 'EUR'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        response_data = response.json()
        self.assertEqual(response_data['currency_pair'], 'USDEUR')
        self.assertEqual(round(float(response_data['exchange_rate']), 1), 1.1)

    def test_currency_pair_view_not_found(self):
        response = self.client.get(
            reverse('currency_exchange_rate', kwargs={'currency_from': 'USD', 'currency_to': 'GBP'}))
        self.assertEqual(response.status_code, 404)
