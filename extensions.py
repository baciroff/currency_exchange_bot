import requests
import json
from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(values):

        if len(values) != 3:
            raise APIException('Слишком много параметров.')
        quote, base, amount = values

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {quote}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту! {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту! {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество! {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = (json.loads(r.content)[base_ticker]) * amount

        return round(total_base, 3)
