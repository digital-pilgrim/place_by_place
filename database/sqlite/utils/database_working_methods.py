from typing import TypeVar, List

from database.sqlite.core import crud


db_write = crud.create()
db_read = crud.retrieve()

T = TypeVar('T')


class HistoryMethods:
    """ Класс, описывающий методы для работы с таблицей history """

    @classmethod
    def write_history(cls,
                      db_model: T,
                      model_name: str,
                      columns: str,
                      data: str) -> None:
        """
        Метод, позволяющий создать запись в модели базы данных

        :param db_model: модель базы данных
        :type db_model: T
        :param model_name: название модели базы данных
        :type model_name: str
        :param columns: поля модели базы данных
        :type columns: str
        :param data: данные для записи
        :type data: str
        """

        db_write(db_model, model_name, columns, data)

    @classmethod
    def get_history_retrieved(cls, db_model: T, columns: str, model_name: str, user_id: int) -> List:
        """
        Метод, позволяющий прочитать записи из модели базы данных

        :param db_model: модель базы данных
        :type db_model: T
        :param columns: поля модели базы данных
        :type columns: str
        :param model_name: название модели базы данных
        :type model_name: str
        :param user_id: id пользователя
        :type user_id: int
        :return: retrieved
        :rtype: List
        """

        retrieved = db_read(db_model, columns, model_name, user_id)

        return retrieved


history_methods = HistoryMethods
