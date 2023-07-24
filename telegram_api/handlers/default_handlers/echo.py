from telebot.types import Message

from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    """
    Хэндлер.
    Направляет пользователя в справку, если тот
    отправил боту текстовое сообщение без указанного состояния.

    :param message: сообщение
    :type message: Message
    """

    text = 'Прошу прощения, но я вас не понимаю. Отправьте команду /help для получения справки'

    bot.send_message(chat_id=message.from_user.id, text=text)
