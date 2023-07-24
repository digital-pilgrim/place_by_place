from datetime import datetime

from telebot.types import Message

from loader import bot

from site_api.core import params

from database.peewee.common.models import db
from database.peewee.utils.database_working_methods import location_methods
from database.peewee.common.models import location_model

from database.sqlite.common.models import history_model
from database.sqlite.utils.database_working_methods import history_methods

from telegram_api.states.custom_commands_states.custom_command_states import SearchStates
from site_api.utils.output_data_generator import specified_range_places

from telegram_api.handlers.custom_handlers.utils.search_result_processor import search_result_processor


place = ''

min_distance = 0
max_distance = 0


@bot.message_handler(commands=['custom'])
def cmd_start(message: Message) -> None:
    """
    Хэндлер.
    Срабатывает, если пользователь отправил команду /custom.
    В зависимости от того, есть ли в базе данных
    геопозиция пользователя, просит её отправить,
    либо переходит к следующему хэндлеру.

    :param message: сообщение
    :type message: Message
    """

    location_retrieved = location_methods.get_location_retrieved()

    user = message.from_user.id

    with db:
        query = location_model.select().where(location_model.user_id == user)

    if not query.exists():
        text = 'Чтобы я знал, где вы находитесь, отправьте команду /location'
        bot.send_message(chat_id=message.from_user.id, text=text)

    else:
        for i_record in location_retrieved:
            if i_record.user_id == user:

                location = i_record.user_location
                location = location.translate({ord(i_sym): None for i_sym in [',', '(', ')']})
                location = location.split()

                latitude, longitude = map(lambda elem: elem, location)

                params['lat'] = latitude
                params['lng'] = longitude

        text = 'Окей! Введите, какое место вас интересует'
        bot.send_message(chat_id=message.from_user.id, text=text)

        bot.set_state(message.from_user.id, SearchStates.custom_cmd_category, message.chat.id)


@bot.message_handler(state=SearchStates.custom_cmd_category)
def get_category(message: Message) -> None:
    """
    Хэндлер.
    Получает от пользователя категорию места,
    которое он хочет найти.
    Если сообщение пользователя корректно,
    переходит к следующему хэндлеру.

    :param message: сообщение
    :type message: Message
    """

    if not message.text.isdigit():
        global place
        place = message.text

        text = 'Запомнил! А теперь укажите в метрах минимальное расстояние поиска'
        bot.send_message(chat_id=message.from_user.id, text=text)

        bot.set_state(message.from_user.id, SearchStates.custom_cmd_min_distance, message.chat.id)

        params['query'] = message.text

    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, используйте буквы')


@bot.message_handler(state=SearchStates.custom_cmd_min_distance)
def get_min_distance(message: Message) -> None:
    """
    Хэндлер.
    Получает от пользователя минимальное расстояние,
    на котором будет вестись поиск.
    Если сообщение пользователя корректно,
    переходит к следующему хэндлеру.

    :param message: сообщение
    :type message: Message
    """

    if message.text.isdigit():
        text = 'Записал! А теперь введите в метрах максимальное расстояние поиска'
        bot.send_message(chat_id=message.from_user.id, text=text)

        bot.set_state(message.from_user.id, SearchStates.custom_cmd_max_distance, message.chat.id)

        global min_distance
        min_distance = int(message.text)

    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, используйте цифры')


@bot.message_handler(state=SearchStates.custom_cmd_max_distance)
def get_max_distance(message: Message) -> None:
    """
    Хэндлер.
    Получает от пользователя максимальное расстояние,
    на котором будет вестись поиск.
    Если сообщение пользователя корректно,
    переходит к следующему хэндлеру.

    :param message: сообщение
    :type message: Message
    """

    if message.text.isdigit():
        text = 'Окей! А теперь укажите, сколько мест вам показать'
        bot.send_message(chat_id=message.from_user.id, text=text)

        bot.set_state(message.from_user.id, SearchStates.custom_cmd_results_quantity, message.chat.id)

        global max_distance
        max_distance = int(message.text)

    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, используйте цифры')


@bot.message_handler(state=SearchStates.custom_cmd_results_quantity)
def get_results_quantity(message: Message) -> None:
    """
    Хэндлер.
    Получает от пользователя количество мест,
    которое он хочет получить.
    Если сообщение пользователя корректно,
    отправляет ему ответ с результатами поиска.

    :param message: сообщение
    :type message: Message
    """

    if message.text.isdigit():
        places_to_show_quantity = int(message.text)

        if not 1 <= places_to_show_quantity <= 10:
            text = 'Я могу найти от 1 до 10 мест'
            bot.send_message(chat_id=message.from_user.id, text=text)
        else:
            if places_to_show_quantity > 1:
                params['limit'] = places_to_show_quantity * 3

            text = 'Ищу...'
            bot.send_message(chat_id=message.from_user.id, text=text)

            results = specified_range_places(limit=places_to_show_quantity,
                                             min_distance=min_distance,
                                             max_distance=max_distance).search_for_specified_range_places()

            search_result = ''
            if results is not None:
                last_place_index = len(results) - 1
                for i_place in results:
                    place_data = search_result_processor.get_data(place=i_place)

                    place_name = place_data[0]

                    place_index = results.index(i_place)
                    if place_index < last_place_index:
                        place_name = f'{place_name}, '

                    search_result = ''.join([search_result, place_name])

                    search_result_processor.send_message(data=place_data, chat_id=message.from_user.id)

                if len(results) < places_to_show_quantity:
                    text = 'Это всё, что удалось найти'
                    bot.send_message(chat_id=message.from_user.id, text=text)

            else:
                search_result = '—'

                text = 'Не нашёл ничего подходящего.\n' \
                       '\n' \
                       'Попробуйте изменить команду или указать другие параметры поиска'
                bot.send_message(chat_id=message.from_user.id, text=text)

            text = 'Для продолжения выберите одну из команд в меню'
            bot.send_message(chat_id=message.from_user.id, text=text)

            db_model = history_model
            model_name = 'history'
            columns = '(created_at, user_id, command_type, place_category, search_result)'
            current_datetime = datetime.strftime(datetime.now(), '%d/%m/%y %H:%M:%S')

            data = f"('{current_datetime}', {message.from_user.id}, '/custom', '{place}', '{search_result}')"

            history_methods.write_history(db_model=db_model,
                                          model_name=model_name,
                                          columns=columns,
                                          data=data)

            bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)

    else:
        text = 'Пожалуйста, используйте цифры'
        bot.send_message(chat_id=message.from_user.id, text=text)
