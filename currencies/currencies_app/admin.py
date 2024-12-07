from django.contrib import admin
from .models import Currency, ExchangeRate

class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("currency_from", "currency_to", "exchange_rate", "updated_at")
    list_filter = ('currency_from', 'currency_to')
    search_fields = ('currency_from__code', 'currency_to__code')
    ordering = ('-updated_at',)

admin.site.register(Currency)
admin.site.register(ExchangeRate, ExchangeRateAdmin)