import yfinance
import mysql.connector
from decouple import config
from currencies_app.models import Currency

currency_pairs = ['EURUSD', 'USDJPY', 'PLNUSD']
exchange_rates = {}

for pair in currency_pairs:
    ticker = yfinance.Ticker(pair)
    data = ticker.history(period="1d")
    exchange_rates[pair] = data['Close'].iloc[-1]

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=config('DB_PASSWORD'),
    database="rates"
)
cursor = db.cursor()

for pair in currency_pairs:
    currency_from = pair[:3]
    currency_to = pair[3:]
    print(currency_from, currency_to)

    currency_from_exists = Currency.objects.filter(code=currency_from).exists()
    currency_to_exists = Currency.objects.filter(code=currency_to).exists()

    if not currency_from_exists or not currency_to_exists:
        continue

    exchange_rate = exchange_rates.get(pair)

    if exchange_rate:
        cursor.execute("""
            UPDATE exchange_rates 
            SET exchange_rate = %s, updated_at = CURRENT_TIMESTAMP 
            WHERE currency_from = %s AND currency_to = %s;
        """, (exchange_rate, currency_from, currency_to))

db.commit()
cursor.close()
db.close()
