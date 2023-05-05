import json
import requests
from config import exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        url = (f"https://api.apilayer.com/exchangerates_data/latest?symbols={sym_key}&base={base_key}")

        payload = {}
        headers= {
         "apikey": ""
        }

        response = requests.request("GET", url, headers=headers, data = payload)

        status_code = response.status_code
        resp = json.loads(response.content)
        new_price = resp['rates'][sym_key] * amount
        print(new_price)
        message = f"Цена {amount} {base_key} в {sym_key} : {new_price}"
        print(message)
        return message
