import os

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings, SecretStr, StrictStr


if not find_dotenv():
    print('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()


class SiteSettings(BaseSettings):
    """
    Класс, выступающий в роли обёртки
    для получения ключа и хоста API
    """

    api_key: SecretStr = os.getenv('API_KEY', None)
    api_host: StrictStr = os.getenv('API_HOST', None)


class BotSettings(BaseSettings):
    """
    Класс, выступающий в роли обёртки
    для получения токена бота
    """

    bot_token: SecretStr = os.getenv('BOT_TOKEN', None)


commands = (
    ('location', 'Местоположение'),
    ('low', 'Ближайшие места'),
    ('high', 'Наиболее отдалённые места'),
    ('custom', 'Места на указанном расстоянии'),
    ('history', 'История поиска'),
    ('help', 'Справка')
)
