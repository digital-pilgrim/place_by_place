from telebot.types import Message

from loader import bot

from database.peewee.common.models import db, location_model
from database.peewee.utils.database_working_methods import location_methods

from telegram_api.keyboards.reply.get_user_location import request_location
from telegram_api.states.default_commands_states.location_command_states import SearchStates


@bot.message_handler(commands=['location'])
def cmd_start(message: Message) -> None:
    """
    Хэндлер.
    Запрашивает у пользователя его геопозицию,
    если тот отправил команду /location.

    :param message: сообщение
    :type message: Message
    """

    text = 'Включите режим передачи геоданных на вашем устройстве ' \
           'и нажмите на кнопку "Отправить геопозицию"'

    bot.send_message(message.from_user.id, text, reply_markup=request_location())

    bot.set_state(message.from_user.id, SearchStates.get_user_location, message.chat.id)


@bot.message_handler(content_types=['text', 'location'], state=SearchStates.get_user_location)
def bot_location(message: Message) -> None:
    """
    Хэндлер.
    Если полученная геопозиция пользователя
    является корректной, добавляет её в базу данных.

    :param message: сообщение
    :type message: Message
    """

    user = message.from_user.id

    if message.content_type == 'location':
        location = (message.location.latitude, message.location.longitude)

        data = [{'user_id': user, 'user_location': location}]

        with db:
            query = location_model.select().where(location_model.user_id == user)

        if not query.exists():
            text = 'Спасибо, получил! Теперь вам доступны команды для поиска мест'

            location_methods.write_location(data=data)
        else:
            text = 'Отлично, обновил!'

            location_methods.update_location(user_id=user, user_location=location)

        bot.set_state(message.from_user.id, None, message.chat.id)

    else:
        text = 'Чтобы отправить данные о местоположении, включите, пожалуйста, ' \
               'режим передачи геоданных на вашем устройстве ' \
               'и нажмите на кнопку "Отправить геопозицию"'

    bot.send_message(chat_id=message.from_user.id, text=text)
