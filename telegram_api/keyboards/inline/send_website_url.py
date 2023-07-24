from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_website(url: str) -> InlineKeyboardMarkup:
    """
    Функция.
    Создаёт inline-кнопку для перехода на сайт организации

    :param url: адрес сайта
    :type url: str
    :return: keyboard
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()

    text = 'Перейти на сайт'
    website = InlineKeyboardButton(text=text, url=url)

    keyboard.add(website)
    return keyboard
