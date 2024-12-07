from django.shortcuts import render
from currencies_app.models import Currency, ExchangeRate
from django.http import JsonResponse
from django.http import Http404

# View for listing all currencies
def CurrencyListView(request):
    currencies = Currency.objects.all()
    currency_data = [{'code': currency.code} for currency in currencies]
    return JsonResponse(currency_data, safe=False)

# View for fetching the latest exchange rate for a specific currency pair
def CurrencyPairView(request, currency_from, currency_to):
    try:
        exchange_rate = ExchangeRate.objects.filter(currency_from__code=currency_from, currency_to__code=currency_to).latest('updated_at')
        return JsonResponse({
            'currency_pair': f'{currency_from}{currency_to}',
            'exchange_rate': str(exchange_rate.exchange_rate)
        })
    except ExchangeRate.DoesNotExist:
        raise Http404(f'Exchange rate not found for {currency_from} to {currency_to}')
