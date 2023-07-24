from telebot.handler_backends import State, StatesGroup


class SearchStates(StatesGroup):
    """
    Класс.
    Описывает состояния команды /high

    Attributes:
        high_cmd_category (State): состояние запроса места
        high_cmd_results_quantity (State): состояние запроса желаемого количества результатов
    """

    high_cmd_category = State()
    high_cmd_results_quantity = State()
