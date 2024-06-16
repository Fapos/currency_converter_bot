import re

from telebot.async_telebot import AsyncTeleBot
from telebot import types
from telebot.types import ChatJoinRequest

from extensions import *


class Handlers:
    def __init__(self, config, locales, currency_list, bot):
        self.config = config
        self.locales = locales
        self.currency_list = currency_list
        self.bot = bot

    async def start_handler(self, message: types.Message, bot: AsyncTeleBot):
        await bot.send_message(message.chat.id, self.locales['welcome'])

    async def help_handler(self, message: types.Message, bot: AsyncTeleBot):
        await bot.send_message(message.chat.id, self.locales['help'])

    async def values_handler(self, message: types.Message, bot: AsyncTeleBot):
        curr_list = ''
        for el in self.currency_list:
            curr_list += f'{el} - {self.currency_list[el]}\n'
        await bot.send_message(message.chat.id, curr_list)

    async def data_handler(self, message: types.Message, bot: AsyncTeleBot):
        api = API()
        _from, _to, _amount = message.text.split(' ')
        try:
            if float(_amount) <= 0:
                raise ValidationError('Введите количество валюты больше нуля.')
            if _from not in self.currency_list.values():
                raise ValidationError(
                    'Неверное значение первой валюты, введите команду /values, чтобы увидеть список доступных валют'
                )

            if _to not in self.currency_list.values():
                raise ValidationError(
                    'Неверное значение второй валюты, введите команду /values, чтобы увидеть список доступных валют'
                )
            await bot.send_message(message.chat.id, str(api.get_price(_from, _to, float(_amount))))
        except ValidationError as exc:
            await bot.send_message(message.chat.id, str(exc))

    def register_handlers(self):
        self.bot.get_bot().register_message_handler(
            self.start_handler,
            func=lambda message: message.text == '/start',
            pass_bot=True
        )
        self.bot.get_bot().register_message_handler(
            self.help_handler,
            func=lambda message: message.text == '/help',
            pass_bot=True
        )
        self.bot.get_bot().register_message_handler(
            self.values_handler,
            func=lambda message: message.text == '/values',
            pass_bot=True
        )
        self.bot.get_bot().register_message_handler(
            self.data_handler,
            func=lambda message: re.match(r'\w{3}\s\w{3}\s\d*', message.text),
            pass_bot=True
        )
