import json
import logging
import telebot

from telebot.async_telebot import AsyncTeleBot, ExceptionHandler
from pathlib import Path
from model import *
from handlers import Handlers


class Bot:
    """
    Класс бота
    """
    def __init__(self, config_path: Path):
        self.config = BotConfig.model_validate_json((config_path / 'config.json').read_text(encoding='utf-8'))
        self.locales = json.loads((config_path / 'locales.json').read_text(encoding='utf-8'))
        self.currency_list = json.loads((config_path / 'currency_list.json').read_text(encoding='utf-8'))
        self.bot = AsyncTeleBot(self.config.telegram_api)
        self.handlers = Handlers(self.config, self.locales, self.currency_list, self)
        self.handlers.register_handlers()

    def get_bot(self):
        return self.bot

    async def start(self):
        await self.bot.polling()


