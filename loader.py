from telebot import TeleBot
from telebot.storage import StateMemoryStorage

from config_data.config import BotSettings


storage = StateMemoryStorage()

bot_settings = BotSettings()

bot_token = bot_settings.bot_token.get_secret_value()

bot = TeleBot(token=bot_token, state_storage=storage)
