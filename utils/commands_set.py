from telebot import TeleBot
from telebot.types import BotCommand

from config_data.config import commands


def commands_set(bot: TeleBot) -> None:
    """
    Функция для получения стандартных команд бота

    :param bot: бот
    :type bot: Telebot
    """

    bot.set_my_commands(
        [BotCommand(*i_command) for i_command in commands]
    )
