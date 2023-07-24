from datetime import datetime

import peewee as pw


db = pw.SqliteDatabase('location.db')


class ModelBase(pw.Model):
    """
    Класс, описывающий создание базовой модели

    Attributes:
        created_at(DateField): время создания записи в базе данных
    """

    created_at = pw.DateField(default=datetime.now())

    class Meta:
        database = db


class Location(ModelBase):
    """
    Класс, описывающий создание таблицы location

    Attributes:
        user_id(int): id пользователя
        user_location(str): географические координаты местоположения пользователя
    """

    user_id = pw.IntegerField()
    user_location = pw.TextField()


location_model = Location
