from django.shortcuts import render
from currencies_app.models import Currency, ExchangeRate
from django.http import JsonResponse, Http404
from rest_framework import viewsets
from .serializers import CurrencySerializer, ExchangeRateSerializer

# View for listing all currencies
def CurrencyListView(request):
    if request.method == 'GET':
        currencies = Currency.objects.all()
        currency_data = [{'code': currency.code} for currency in currencies]
        return JsonResponse(currency_data, safe=False)
    else:
        return JsonResponse({'error': 'GET method required'}, status=405)

def CurrencyPairView(request, currency_from, currency_to):
    try:
        exchange_rate = ExchangeRate.objects.filter(currency_from__code=currency_from, currency_to__code=currency_to).latest('updated_at')
        return JsonResponse({
            'currency_pair': f'{currency_from}{currency_to}',
            'exchange_rate': str(exchange_rate.exchange_rate)
        })
    except ExchangeRate.DoesNotExist:
        raise Http404(f'Exchange rate not found for {currency_from} to {currency_to}')

def HomeView(request):
    return render(request, 'home.html')

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class ExchangeRateViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer