from typing import List, Tuple

from peewee import ModelSelect

from database.peewee.common.models import db, location_model
from database.peewee.core import crud


db_write = crud.create()
db_read = crud.retrieve()
db_update = crud.update()


class LocationMethods:
    """ Класс, описывающий методы для работы с таблицей location """

    @classmethod
    def write_location(cls, data: List) -> None:
        """
        Метод, позволяющий создать запись в модели базы данных

        :param data: данные для записи
        :type data: List
        """

        db_write(db, location_model, data)

    @classmethod
    def get_location_retrieved(cls) -> ModelSelect:
        """
        Метод, позволяющий прочитать записи из модели базы данных

        :return: retrieved
        :rtype: ModelSelect
        """

        retrieved = db_read(db, location_model, location_model.user_id, location_model.user_location)

        return retrieved

    @classmethod
    def update_location(cls, user_id: int, user_location: Tuple) -> None:
        """
        Метод, позволяющий обновить запись в модели базы данных

        :param user_id: id пользователя
        :type user_id: int
        :param user_location: координаты местоположения пользователя
        :type user_location: Tuple
        """

        db_update(db, location_model, (location_model.user_id, location_model.user_location), (user_id, user_location))


location_methods = LocationMethods
