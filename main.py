from telebot.custom_filters import StateFilter

from loader import bot

from utils.commands_set import commands_set

from telegram_api import handlers


if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    commands_set(bot)
    bot.infinity_polling()
