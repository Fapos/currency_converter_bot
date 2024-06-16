from pydantic import BaseModel


class BotConfig(BaseModel):
    telegram_api: str
