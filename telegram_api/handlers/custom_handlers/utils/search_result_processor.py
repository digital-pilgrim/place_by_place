from typing import Dict, Tuple

from loguru import logger

from loader import bot

from telegram_api.keyboards.inline.send_website_url import get_website


logger.add(
    'debug.log',
    format='{time} {level} {message}',
    level='DEBUG',
    rotation='1 week'
)


class SearchResultProcessor:
    """
    Класс.
    Выполняет роль обёртки для двух функций.
    """

    @classmethod
    @logger.catch
    def get_data(cls, place: Dict) -> Tuple:
        """
        Метод.
        Собирает и возвращает информацию о месте.

        :param place: место
        :type place: Dict
        :return: data
        :rtype: Tuple
        """

        name = place['name']
        owner_name = place['owner_name']

        if name is not None:
            name = name
        elif owner_name is not None:
            name = owner_name
        else:
            name = '—'

        address = place['address']
        full_address = place['full_address']

        if address is None:
            if full_address is not None:
                address = full_address
            else:
                address = '—'

        latitude = place['latitude']
        longitude = place['longitude']

        phone_number = place['phone_number']
        rating = place['rating']
        site = place['website']

        if site is not None:
            keyboard = get_website(url=site)
        else:
            keyboard = None

        distance = place['distance']

        if place['photos_sample'] is not None:
            video = place['photos_sample'][0]['video_thumbnail_url']
            photo = place['photos_sample'][0]['photo_url']
        else:
            video = None
            photo = None

        data = (name, address, latitude, longitude, phone_number, rating, keyboard, distance, video, photo)

        return data

    @classmethod
    @logger.catch
    def send_message(cls, data: Tuple, chat_id: int) -> None:
        """
        Метод.
        Собирает из данных о месте сообщение
        и отправляет его пользователю.

        :param data: данные о месте
        :type data: Tuple
        :param chat_id: id чата
        :type chat_id: int
        """

        name, address, latitude, longitude, phone_number, rating, keyboard, distance, video, photo = \
            map(lambda elem: elem, data)

        text = f'<b>{name}</b>\n' \
               f'\nАдрес: {address}\n'

        if rating != 0:
            rating_string = f'Рейтинг: {rating}/5\n'
            text = '\n'.join([text, rating_string])

        distance_string = f'До места: {distance} м'
        text = '\n'.join([text, distance_string])

        if phone_number is not None:
            text = '\n\n'.join([text, phone_number])

        map_url = f'<a href="https://maps.yandex.ru/?text={latitude}, {longitude}">Посмотреть на карте</a>'
        text = '\n\n'.join([text, map_url])

        if video is not None:
            bot.send_video(chat_id, video=video, caption=text, reply_markup=keyboard, parse_mode='HTML')
        elif photo is not None:
            bot.send_photo(chat_id, photo=photo, caption=text, reply_markup=keyboard, parse_mode='HTML')
        else:
            bot.send_message(chat_id, text=text, reply_markup=keyboard, parse_mode='HTML')


search_result_processor = SearchResultProcessor
