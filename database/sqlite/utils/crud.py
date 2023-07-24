from typing import TypeVar, List


T = TypeVar('T')


def _storing_data(db_model: T,
                  model_name: str,
                  columns: str,
                  data: str) -> None:
    """
    Функция для реализации хранения данных

    :param db_model: модель базы данных
    :type db_model: T
    :param model_name: название модели базы данных
    :type model_name: str
    :param columns: поля модели базы данных
    :type columns: str
    :param data: данные для хранения
    :type data: str
    """

    with db_model:
        cursor = db_model.cursor()
        cursor.execute(f"INSERT INTO {model_name}{columns} VALUES{data};")

        db_model.commit()


def _retrieve_all_data(db_model: T, columns: str, model_name: str, user_id: int) -> List:
    """
    Функция для реализации чтения данных

    :param db_model: модель базы данных
    :type db_model: T
    :param columns: поля модели базы данных
    :type columns: str
    :param model_name: название модели базы данных
    :type model_name: str
    :param user_id: id пользователя
    :type user_id: int
    :return: response
    :rtype: List
    """

    with db_model:
        cursor = db_model.cursor()

        cursor.execute(f"SELECT {columns} "
                       f"FROM "
                       f"(SELECT * FROM {model_name} "
                       f"WHERE user_id = {user_id}) "
                       f"ORDER BY id DESC LIMIT 10;")

        response = cursor.fetchall()

        return response


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


if __name__ == '__main__':
    _storing_data(db_model=T, model_name='', columns='', data='')
    _retrieve_all_data(db_model=T, columns='', model_name='', user_id=0)

    CRUDInterface()
