### Проект: "social_blog"
### 1. Описание проекта:
social_blog - блог-платформа для мемов, позволяющая пользователям делиться своими мемами, добавлять описание, а так же оставлять комментарии.
### Выполненные задачи:
Подключение кастомных страниц для ошибок, пользователей, пагинации. Изображения к постам, добавление/изменение/удаление публикаций. Создание системы комментирования записей. Отправка электронной почты Ya-SMTP.


### 2. Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Den4u/social_blog.git
```
```
cd social_blog
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
Обновить pip. Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver
```

### Автор: https://github.com/Den4u
