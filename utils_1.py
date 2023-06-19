import requests
import json
from config_1 import exchange


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_convert(curr_from, curr_to, amount):
        if curr_from == curr_to:
            raise ConvertionException(f'Вы пытаетесь перевести одну валюту {curr_from} в саму себя!\n'
                                      f'Для правильного ввода валют воспользуйтесь клавиатурой /convert\n'
                                      f'помощь /help')

        try:
            curr_from_mean = exchange[curr_from]

        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {curr_from}!\n'
                                      f'Список доступных валют /values\n'
                                      f'Ввести нужные валюты заново /convert\n'
                                      f'помощь /help')

        try:
            curr_to_mean = exchange[curr_to]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {curr_to}!\n'
                                      f'Список доступных валют /values\n'
                                      f'Ввести нужные валюты заново /convert\n'
                                      f'помощь /help')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество: {amount}\n'
                                      f'Список доступных валют /values\n'
                                      f'Ввести нужные валюты заново /convert\n'
                                      f'помощь /help')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={curr_from_mean}&tsyms={curr_to_mean}')

        total_base = json.loads(r.content)[exchange[curr_to]] * amount

        return round(total_base, 2)
