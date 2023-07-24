from telebot.handler_backends import State, StatesGroup


class SearchStates(StatesGroup):
    """
    Класс.
    Описывает состояния команды /location

    Attributes:
         get_user_location (State): состояние запроса геопозиции пользователя
    """

    get_user_location = State()
