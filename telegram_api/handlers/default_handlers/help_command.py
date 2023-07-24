from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    """
    Хэндлер.
    Выводит пользователю справку,
    если тот отправил команду /help

    :param message: сообщение
    :type message: Message
    """

    text = 'Для поиска боту необходимо знать, где вы находитесь, ' \
           'а так же категорию места, в которое вы хотите сходить — ресторан, кинотеатр, магазин и так далее.\n' \
           '\n' \
           'Ниже представлены команды, с помощью которых вы можете взаимодействовать с ботом:\n' \
           '\n' \
           '/location — сообщить боту, где вы находитесь\n' \
           '\n' \
           '/low — найти ближайшие к вам места\n' \
           '\n' \
           '/high — найти наиболее отдалённые от вас места\n' \
           '\n' \
           '/custom — найти места на интересующем вас расстоянии\n' \
           '\n' \
           '/history — посмотреть историю поиска\n' \
           '\n' \
           '/help — получить справку'

    bot.send_message(chat_id=message.from_user.id, text=text, parse_mode='HTML')
