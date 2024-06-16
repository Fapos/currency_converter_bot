import requests
import xmltodict
import json

from typing import Any
from errors import *


class API:
    """
    Класс работы с внешними апи.
    """

    def __init__(self):
        ...

    def get_price(self, _base: str, _quote: str, _amount: float) -> float:
        """
        Метод получения конвертированной валюты.
        :param _base: имя валюты, цену на которую надо узнать.
        :param _quote: имя валюты, цену в которой надо узнать.
        :param _amount: количество переводимой валюты.
        :return: Цена переводимой валюты в целевой.
        """

        base_url = r"https://v6.exchangerate-api.com/v6/09cb19a7dbe6be6c04d5ec95/latest/"

        main_url = base_url + _base
        try:
            with requests.Session() as s:
                data = s.get(main_url).json()

            result = data['conversion_rates'][_quote] * _amount
            return result
        except (KeyError, requests.exceptions.JSONDecodeError):
            raise ValidationError('Неверные входные данные, попробуйте еще раз.')

