from typing import List


def history_message_collector(user_records: List) -> str:
    """
    Функция.
    Собирает и возвращает сообщение с историей запросов пользователя.

    :param user_records: запросы пользователя
    :type user_records: List
    :return: text
    :rtype: str
    """

    text = 'Ваши последние запросы:\n\n'

    for i_record in user_records:
        date, command, place, search_result = map(lambda column: column, i_record)
        query = f'Дата и время запроса: {date}\n' \
                f'Команда: {command}\n' \
                f'Место: {place}\n' \
                f'Результат: {search_result}\n\n'

        text = ''.join([text, query])

    return text
