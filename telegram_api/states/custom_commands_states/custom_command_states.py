from telebot.handler_backends import State, StatesGroup


class SearchStates(StatesGroup):
    """
    Класс.
    Описывает состояния команды /custom

    Attributes:
        custom_cmd_category (State): состояние запроса места
        custom_cmd_min_distance (State): состояние запроса минимального расстояния, на котором будет вестись поиск
        custom_cmd_max_distance (State): состояние запроса максимального расстояния, на котором будет вестись поиск
        custom_cmd_results_quantity (State): состояние запроса желаемого количества результатов
    """

    custom_cmd_category = State()
    custom_cmd_min_distance = State()
    custom_cmd_max_distance = State()
    custom_cmd_results_quantity = State()
