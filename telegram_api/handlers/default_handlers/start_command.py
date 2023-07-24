from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """
    Хэндлер.
    Приветствует пользователя, если тот
    отправил команду /start

    :param message: сообщение
    :type message: Message
    """

    text = f"Здравствуйте, {message.from_user.full_name}!\n"\
           f"\n"\
           f"Скажите мне, что хотите посетить, а я найду подходящие варианты вокруг вас.\n" \
           f"\n"\
           f"Для продолжения отправьте команду /help"

    bot.send_message(chat_id=message.from_user.id, text=text)
