![workflow](https://github.com/petrushque/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# foodgram

Проект Foodgram.\
«Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты,
добавлять чужие рецепты в избранное и подписываться на публикации других авторов.
Сервис «Список покупок» позволит пользователям создавать список продуктов,
которые нужно купить для приготовления выбранных блюд.

Проект доступен по адресу http://84.252.141.163/

## Технологии
- [Django] - Бэкэнд фреймворк
- [Django Rest Framework] - Фрэймворк для создания API на основе Django
- [Djoser] - Библиотека для авторизации
- [Django Filter] - Библиотека для фильтрации данных
- [Pillow] - Библиотека для обработки изображений
- [Reportlab] - Библиотека для создания PDF документов
- [Docker] - ПО для развертывания в контейнере
- [Reactjs] - Фронтэнд фреймворк
- [Gunicorn] - WSGI веб-сервер
- [Postgresql] - База данных
- [Nginx] - HTTP Веб-сервер

## Установка

### Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:PETRUSHQUE/foodgram-project.git
```
```
cd foodgram-project
```
### Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
. venv/Scripts/activate
```
### Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r backend/foodgram/requirements.txt
```
### Наполнить .env файл
```
cd backend

DB_ENGINE=<...> # указываем, что работаем с postgresql
DB_NAME=<...> # имя базы данных
POSTGRES_USER=<...> # логин для подключения к базе данных
POSTGRES_PASSWORD=<...> # пароль для подключения к БД (установите свой)
DB_HOST=<...> # название сервиса (контейнера)
DB_PORT=<...> # порт для подключения к БД
SECRET_KEY=<...>	# ключ для settings.py
```
### Перейти в папку с docker-compose.yml и собрать контейнеры:
```
cd ../infra
docker-compose up -d --build
```
### Создать миграции, провести их, собрать статику, создать суперюпользователя
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py createsuperuser
```
### Наполнить БД ингредиентами из CSV файла (при необходимости)
```
docker-compose exec web bash
export DJANGO_SETTINGS_MODULE=foodgram.settings
python db_populate.py
```
## Примеры запросов к API и ответов
### Доступно на http://localhost/api/docs/

[//]: # 

   [Django]: <https://www.djangoproject.com/>
   [Django Rest Framework]: <https://www.django-rest-framework.org/>
   [Django Filter]: <https://github.com/carltongibson/django-filter/>
   [Djoser]: <https://github.com/sunscrapers/djoser/>
   [Pillow]: <https://python-pillow.org/>
   [Reportlab]: <http://www.reportlab.com/>
   [Docker]: <https://www.docker.com/>
   [Gunicorn]: <https://gunicorn.org/>
   [Postgresql]: <https://www.postgresql.org/>
   [Nginx]: <https://nginx.org/>
   [Reactjs]: <https://reactjs.org/>