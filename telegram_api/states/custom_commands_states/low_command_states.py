from telebot.handler_backends import State, StatesGroup


class SearchStates(StatesGroup):
    """
    Класс.
    Описывает состояния команды /low

    Attributes:
        low_cmd_category (State): состояние запроса места
        low_cmd_results_quantity (State): состояние запроса желаемого количества результатов
    """

    low_cmd_category = State()
    low_cmd_results_quantity = State()
