# Currency Exchange Database API
## Overview
This project provides a simple REST API for currency exchange rates. It stores currency codes and their respective exchange rates in a MySQL database. Users can fetch the latest exchange rates between different currencies.

## Features
- List all currencies: Retrieve a list of all currencies available in the database.
- Get latest exchange rate: Fetch the latest exchange rate for a specific currency pair (e.g., USD to EUR).
- Data Source: The exchange rates are fetched and stored using an external source, yfinance 

## API Endpoints
### GET /currency/
Description: Fetches a list of all available currencies in the database.
### GET /currency/{currency_from}/{currency_to}/
Description: Fetches the latest exchange rate for the given currency pair 
### Combinations
- /currency/EUR/USD/
- /currency/USD/JPY/
- /currency/PLN/USD/
