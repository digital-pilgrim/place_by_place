# Place by place

Place by place - это телеграм-бот, находящий 
вокруг пользователя интересующие его места.  

Пользователь отправляет команду, от которой зависит, 
на каком расстоянии будет вестись поиск, а затем вводит, 
что и в каком количестве хочет найти. 

Далее, бот показывает изображение каждого из найденных мест и
общую информацию о нём.


## Дополнительная документация:
* [Проблема, которую решает проект](docs/another_docs/problem_and_solution.md)  
* [Используемые сервисы](docs/another_docs/services_used.md)  
* [Взаимодействие бота с пользователем](docs/another_docs/bot_algorithm.md)

В проекте используется СУБД SQLite и ORM Peewee.

## Сборка репозитория и локальный запуск
Выполните в терминале:
```
git clone https://github.com/egrorik/place_by_place.git
pip install -r requirements.txt
```
 
### Настройка
Создайте файл .env и добавьте туда следующие настройки:
```
BOT_TOKEN='Ваш токен для бота, полученный от @BotFather'

API_KEY='Ваш ключ, полученный от API по адресу https://local-business-data.p.rapidapi.com/search-nearby'
API_HOST='Ваш хост, полученный от API по адресу https://local-business-data.p.rapidapi.com/search-nearby'

```

### Запуск
Чтобы запустить бота, выполните в терминале:
```
python3 main.py
```
