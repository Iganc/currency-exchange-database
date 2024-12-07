from django.core.management.base import BaseCommand
import yfinance as yf
from currencies_app.models import Currency, ExchangeRate

class Command(BaseCommand):
    help = "Fetch and update exchange rates"

    def handle(self, *args, **kwargs):
        currency_pairs = ['EURUSD=X', 'USDJPY=X', 'PLNUSD=X']
        exchange_rates = {}

        for pair in currency_pairs:
            ticker = yf.Ticker(pair)
            data = ticker.history(period="1d")
            if not data.empty:
                exchange_rates[pair] = data['Close'].iloc[-1]

        for pair in currency_pairs:
            currency_from = pair[:3]
            currency_to = pair[3:6]

            try:
                currency_from_obj = Currency.objects.get(code=currency_from)
                currency_to_obj = Currency.objects.get(code=currency_to)
            except Currency.DoesNotExist:
                self.stdout.write(f"Currency {currency_from} or {currency_to} not found in the database.")
                continue

            exchange_rate = exchange_rates.get(pair)

            if exchange_rate:
                exchange_rate_obj, created = ExchangeRate.objects.update_or_create(
                    currency_from=currency_from_obj,
                    currency_to=currency_to_obj,
                    defaults={'exchange_rate': exchange_rate}
                )
                if created:
                    self.stdout.write(f"Created new exchange rate: {currency_from} -> {currency_to}")
                else:
                    self.stdout.write(f"Updated exchange rate: {currency_from} -> {currency_to}")
