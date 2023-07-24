from typing import Dict, Union

import requests


def _make_response(url: str,
                   headers: Dict,
                   params: Dict,
                   timeout: int,
                   success: int = 200) -> Union[requests.models.Response, int]:
    """
    Универсальная функция для реализации запросов в дочерних функциях

    :param url: адрес, по которому будет выполнен запрос
    :type url: str
    :param headers: заголовки запроса
    :type headers: Dict
    :param params: параметры запроса
    :type params: Dict
    :param timeout: максимальное время ожидания ответа
    :type timeout: int
    :param success: код успешного запроса
    :type success: int
    :return: response or status_code
    :rtype: Union[requests.models.Response, int]
    """

    response = requests.get(url=url, headers=headers, params=params, timeout=timeout)

    status_code = response.status_code

    if status_code == success:
        return response

    return status_code


def _search_nearby(url: str,
                   headers: Dict,
                   params: Dict,
                   timeout: int,
                   func=_make_response) -> requests.models.Response:
    """
    Функция для реализации запроса через универсальную функцию

    :param url: адрес, по которому будет выполнен запрос
    :type url: str
    :param headers: заголовки запроса
    :type headers: Dict
    :param params: параметры запроса
    :type params: Dict
    :param timeout: максимальное время ожидания ответа
    :type timeout: int
    :return: response or status_code
    :rtype: Union[requests.models.Response, int]
    """

    response = func(url, headers=headers, params=params, timeout=timeout)

    return response


class SiteAPIInterface:
    """ Класс, выступающий в роли обёртки для дочерних функций """

    @classmethod
    def search_nearby(cls):
        """
        Метод.
        Возвращает функцию _search_nearby

        :return: _search_nearby
        :rtype: function
        """

        return _search_nearby


if __name__ == '__main__':
    _make_response(url='', headers={}, params={}, timeout=0)
    _search_nearby(url='', headers={}, params={}, timeout=0)

    SiteAPIInterface()
