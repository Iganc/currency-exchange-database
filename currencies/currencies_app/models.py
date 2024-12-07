from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.code

class ExchangeRate(models.Model):
    currency_from = models.ForeignKey(Currency, related_name='from_currency', on_delete=models.CASCADE)
    currency_to = models.ForeignKey(Currency, related_name='to_currency', on_delete=models.CASCADE)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=6)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.currency_from.code} to {self.currency_to.code}'