import re

import requests

AVAILABLE_CURRENCIES = "EUR GBP PLN USD"


def _api_request(method, url, params):
    try:
        response = requests.request(method=method, url=url, params=params)
        return response
    except Exception as ex:
        raise Exception(f"Unsuccessful attempt to hit endpoint {url}: {ex}")


def get_user_input():
    base_currency = input(
        f"What is the base currency? Select from: {AVAILABLE_CURRENCIES}\n").upper()
    amount = input("What is the amount to convert?\n")
    conversion_currencies = re.sub(base_currency, '', AVAILABLE_CURRENCIES)
    target_currency = input(
        f"What is the target currency? Select from: {conversion_currencies}\n").upper()
    return {
        'base_currency': base_currency,
        'amount': amount,
        'target_currency': target_currency
    }


def convert_currency(currency_info):
    base = currency_info.get('base_currency')
    target = currency_info.get('target_currency')
    amount = int(currency_info.get('amount'))
    method = 'GET'
    url = 'https://api.exchangeratesapi.io/latest'
    params = {
        'base': base
    }
    response = _api_request(method=method, url=url, params=params)
    rates = response.json()
    fx_rate = rates.get('rates').get(target)
    if fx_rate is not None:
        converted_amount = format(amount * fx_rate, '.2f')
        result = f"{base}{amount} is {target}{converted_amount}"
        print(f"Rate of exchange: {fx_rate}")
        print(result)
    else:
        print("Unable to get fx rate and calculate currency conversion")


def control():
    user_input = get_user_input()
    convert_currency(user_input)


if __name__ == '__main__':
    control()
