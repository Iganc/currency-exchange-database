from django.core.management.base import BaseCommand
import yfinance as yf
from datetime import datetime, timedelta
from currencies_app.models import Currency, ExchangeRate

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        currency_pairs = [
            ('EUR', 'USD'),
            ('USD', 'JPY'),
            ('PLN', 'USD'),
        ]

        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        for currency_from_code, currency_to_code in currency_pairs:
            try:
                symbol = f"{currency_from_code}{currency_to_code}=X"
                data = yf.download(symbol, start=start_date, end=end_date)

                currency_from = Currency.objects.get(code=currency_from_code)
                currency_to = Currency.objects.get(code=currency_to_code)

                for index, row in data.iterrows():
                    try:
                        exchange_rate = float(row['Close'])
                    except ValueError:
                        print(f"Skipping invalid rate data for {currency_from_code}/{currency_to_code} on {index}")
                        continue

                    updated_at = index


                    ExchangeRate.objects.create(
                        currency_from=currency_from,
                        currency_to=currency_to,
                        exchange_rate=exchange_rate,
                        updated_at=updated_at
                    )
                    self.stdout.write(self.style.SUCCESS(f"Saved rate for {currency_from_code}/{currency_to_code} on {updated_at}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching data for {currency_from_code}/{currency_to_code}: {e}"))
