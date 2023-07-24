from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_location() -> ReplyKeyboardMarkup:
    """
    Функция.
    Создаёт reply-кнопку для отправки данных о местоположении пользователя

    :return: keyboard
    :rtype: ReplyKeyboardMarkup
    """

    keyboard = ReplyKeyboardMarkup(True, True)

    text = 'Отправить геопозицию'
    keyboard.add(KeyboardButton(text=text, request_location=True))

    return keyboard
