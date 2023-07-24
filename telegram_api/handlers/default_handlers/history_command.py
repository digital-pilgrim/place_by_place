from telebot.types import Message

from loader import bot

from database.sqlite.common.models import history_model
from database.sqlite.utils.database_working_methods import history_methods

from telegram_api.handlers.default_handlers.utils.history_message_collector import history_message_collector


@bot.message_handler(commands=['history'])
def bot_history(message: Message) -> None:
    """
    Хэндлер.
    Отправляет сообщение с историей запросов пользователя,
    если тот отправил команду /history

    :param message: сообщение
    :type message: Message
    """

    user_records = history_methods.get_history_retrieved(db_model=history_model,
                                                         columns='created_at, '
                                                                 'command_type, '
                                                                 'place_category, '
                                                                 'search_result',
                                                         model_name='history',
                                                         user_id=message.from_user.id)

    if len(user_records) != 0:
        text = history_message_collector(user_records=user_records)

    else:
        text = 'Вы не сделали ни одного запроса'

    bot.send_message(chat_id=message.from_user.id, text=text)
