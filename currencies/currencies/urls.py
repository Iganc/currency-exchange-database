"""
URL configuration for currencies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from currencies_app.views import CurrencyPairView, CurrencyListView, HomeView


urlpatterns = [
    path('', HomeView, name='home'),
    path('admin/', admin.site.urls),
    path('currency/<str:currency_from>/<str:currency_to>/', CurrencyPairView, name='currency_exchange_rate'),
    path('currency/', CurrencyListView, name='currency_list')
]
