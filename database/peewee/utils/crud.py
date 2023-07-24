from typing import TypeVar, List, Dict

from peewee import ModelSelect

from database.peewee.common.models import ModelBase
from database.peewee.common.models import db


T = TypeVar('T')
S = TypeVar('S')


def _storing_data(database: db, model: T, *data: List[Dict]) -> None:
    """
    Функция для реализации хранения данных

    :param database: база данных
    :type database: db
    :param model: модель базы данных
    :type model: T
    :param data: данные для хранения
    :type data: List[Dict]
    """

    with database.atomic():
        model.insert_many(*data).execute()


def _retrieve_all_data(database: db, model: T, *columns: ModelBase) -> ModelSelect:
    """
    Функция для реализации чтения данных

    :param database: база данных
    :type database: db
    :param model: модель базы данных
    :type model: T
    :param columns: поля
    :type columns: ModelBase
    :return: response
    :rtype: ModelSelect
    """

    with database.atomic():
        response = model.select(*columns)

    return response


def _update_data(database: db, model: T, columns: ModelBase, records: ModelBase) -> None:
    """
    Функция для реализации обновления данных

    :param database: база данных
    :type database: db
    :param model: модель базы данных
    :type model: T
    :param columns: поля
    :type columns: ModelBase
    :param records: записи
    :type records: ModelBase
    """

    with database.atomic():
        query = model.update({columns[1]: records[1]}).where(columns[0] == records[0])
        query.execute(database)


class CRUDInterface:
    """ Класс, возвращающий интерфейс для работы с моделью базы данных """

    @classmethod
    def create(cls):
        """
        Метод, возвращающий функцию для хранения данных

        :return: _storing_data
        :rtype: function
        """

        return _storing_data

    @classmethod
    def retrieve(cls):
        """
        Метод, возвращающий функцию для чтения данных

        :return: _retrieve_all_data
        :rtype: function
        """

        return _retrieve_all_data

    @classmethod
    def update(cls):
        """
        Метод, возвращающий функцию для обновления данных

        :return: _update_data
        :rtype: function
        """

        return _update_data


if __name__ == '__main__':
    _storing_data(database=db, model=T)
    _retrieve_all_data(database=db, model=T)
    _update_data(database=db, model=T, columns=S, records=S)

    CRUDInterface()
