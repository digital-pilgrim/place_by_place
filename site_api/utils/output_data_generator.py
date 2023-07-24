from typing import List, Tuple, Dict, Union
from math import ceil

from geopy.distance import geodesic

from site_api.core import url, headers, params, timeout, site_api


class DataProcessor:
    """
    Класс, описывающий обработку API данных

    Args:
        limit (int): количество результатов, которое необходимо вернуть
    """

    def __init__(self, limit):
        self.limit = limit

    @classmethod
    def get_response(cls) -> Dict:
        """
        Метод.
        Получает API данные

        :return: response
        :rtype: Dict
        """

        search_nearby = site_api.search_nearby()

        response = search_nearby(url, headers, params, timeout)

        if type(response) != int:
            response = response.json()
            return response

    def start_process(self) -> List:
        """
        Метод.
        Получает API данные из get_response,
        отбирает из них данные о местах и сортирует их в sorting_data_by_distance

        :return: sorted_data_by_distance
        :rtype: List
        """

        response = self.get_response()

        if response is not None:
            places = response['data']

            if places is not None:
                user_lat = response['parameters']['lat']
                user_lng = response['parameters']['lng']
                user_point = (user_lat, user_lng)

                sorted_data_by_distance = self.sorting_data_by_distance(data=places, user_point=user_point)

                return sorted_data_by_distance

    def sorting_data_by_distance(self, data: List, user_point: Tuple) -> List:
        """
        Метод.
        Получает данные о местах из start_process
        и сортирует их по увеличению расстояния от пользователя до места

        :param data: данные о местах
        :type data: List
        :param user_point: данные о местоположении пользователя
        :type user_point: Tuple
        :return: sorted_data
        :rtype: List
        """

        for i_place in data:
            distance = self.get_distance(place=i_place, user_point=user_point)
            i_place['distance'] = distance

        sorted_data = sorted(data, key=self.distance_sort_key)

        return sorted_data

    def sorting_data_by_rating(self, data: List) -> List:
        """
        Метод.
        Получает данные о местах из метода в подклассе
        и сортирует их по уменьшению значения рейтинга

        :param data: данные о местах
        :type data: List
        :return: sorted_data
        :rtype: List
        """

        for i_place in data:
            if i_place['rating'] is None:
                i_place['rating'] = 0

        sorted_data = sorted(data, key=self.rating_sort_key, reverse=True)

        return sorted_data

    def select_data_by_elements_quantity(self, data) -> List:
        """
        Метод.
        Получает данные о местах из подкласса
        и отбирает места, основываясь на желаемом количестве результатов.

        :param data: данные о местах
        :type data: List
        :return: result
        :rtype: List
        """

        result = []
        for i_place in data:
            if data.index(i_place) <= self.limit - 1:
                result.append(i_place)

        if result is not None:
            return result

    @classmethod
    def get_distance(cls, place: Dict, user_point: Tuple) -> int:
        """
        Метод.
        Получает данные о месте и местоположении пользователя, а потом
        возвращает расстояние от пользователя до места

        :param place: данные о месте
        :type place: Dict
        :param user_point: данные о местоположении пользователя
        :type user_point: Tuple
        :return: distance
        :rtype: int
        """

        place_point = (place['latitude'], place['longitude'])
        distance = int(geodesic(user_point, place_point).meters)
        return distance

    @classmethod
    def distance_sort_key(cls, place: Dict) -> int:
        """
        Метод.
        Получает ключ, по которому будет производиться
        сортировка данных о местах в sorting_data_by_distance

        :param place: данные о месте
        :type place: Dict
        :return: sort_key
        :rtype: int
        """

        sort_key = place['distance']
        return sort_key

    @classmethod
    def rating_sort_key(cls, place: Dict) -> Union[int, float]:
        """
        Метод.
        Получает ключ, по которому будет производиться
        сортировка данных о местах в sorting_data_by_rating

        :param place: данные о месте
        :type place: Dict
        :return: sort_key
        :rtype: Union[int, float]

        """

        sort_key = place['rating']
        return sort_key


class NearestPlaces(DataProcessor):
    """ Подкласс NearestPlaces. Родительский класс: DataProcessor """

    def search_for_nearest_places(self) -> List:
        """
        Метод.
        Получает данные о местах из start_process,
        находит из них ближайшие к пользователю и
        возвращает их в желаемом количестве.

        :return: selected_data_by_elements_quantity
        :rtype: List
        """

        data = self.start_process()

        if data is not None:
            nearest_places_quantity = ceil(len(data) / 3)
            last_nearest_place_index = nearest_places_quantity - 1

            nearest_places = []

            for i_place in data:
                place_index = data.index(i_place)

                distance_valid = place_index <= last_nearest_place_index
                if distance_valid:
                    nearest_places.append(i_place)

            if len(nearest_places) > 0:
                selected_data_by_elements_quantity = self.select_data_by_elements_quantity(data=nearest_places)
                sorting_data_by_rating = self.sorting_data_by_rating(data=selected_data_by_elements_quantity)
                return sorting_data_by_rating


class RemotePlaces(DataProcessor):
    """ Подкласс RemotePlaces. Родительский класс: DataProcessor """

    def search_for_remote_places(self):
        """
        Метод.
        Получает данные о местах из start_process,
        находит из них наиболее отдалённые от пользователя и
        возвращает их в желаемом количестве.

        :return: selected_data_by_elements_quantity
        :rtype: List
        """

        data = self.start_process()

        if data is not None:
            remote_places_quantity = ceil(len(data) / 3)
            first_remote_place_index = len(data) - remote_places_quantity

            remote_places = []

            for i_place in data:
                place_index = data.index(i_place)

                distance_valid = place_index >= first_remote_place_index
                if distance_valid:
                    remote_places.append(i_place)

            if len(remote_places) > 0:
                selected_data_by_elements_quantity = self.select_data_by_elements_quantity(data=remote_places)
                sorting_data_by_rating = self.sorting_data_by_rating(data=selected_data_by_elements_quantity)
                return sorting_data_by_rating


class SpecifiedRangePlaces(DataProcessor):
    """
    Подкласс SpecifiedRangePlaces. Родительский класс: DataProcessor

    Args:
        limit (int): максимальное количество результатов
        min_distance (int): минимальное расстояние, на котором будет вестись поиск
        max_distance (int): максимальное расстояние, на котором будет вестись поиск
    """

    def __init__(self, limit, min_distance, max_distance):
        super().__init__(limit)
        self.min_distance = min_distance
        self.max_distance = max_distance

    def search_for_specified_range_places(self):
        """
        Метод.
        Получает данные о местах из start_process,
        находит из них те, которые попадают
        в диапазон расстояний, указанный пользователем
        и возвращает их в желаемом количестве.

        :return: selected_data_by_elements_quantity
        :rtype: List
        """

        data = self.start_process()

        if data is not None:
            specified_range_places = []

            for i_place in data:
                distance = i_place['distance']

                distance_valid = self.min_distance <= distance <= self.max_distance
                if distance_valid:
                    specified_range_places.append(i_place)

            if len(specified_range_places) > 0:
                selected_data_by_elements_quantity = self.select_data_by_elements_quantity(data=specified_range_places)
                sorting_data_by_rating = self.sorting_data_by_rating(data=selected_data_by_elements_quantity)
                return sorting_data_by_rating


nearest_places = NearestPlaces
remote_places = RemotePlaces
specified_range_places = SpecifiedRangePlaces
