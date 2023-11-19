# Микросервис ресурсов

<p align="center"><img src="static/logo.svg" align="middle" width="25%"></p>

## Введение

Микросервис применяется для контроля производства и распределения ресурсов на основании потребностей пользователей.

## Запуск

Скачивание репозитория:

```sh
git clone https://github.com/your_account/your_repo
```

Установка зависимостей:

```sh
pip install -r requirements.txt
```

Применение миграций:

```sh
python manage.py migrate
```

Заполнить переменные окружения, добавив и заполнив файл `.env`

Запуск сервера:

```sh
python manage.py runserver
```

Проверка доступности сервера:

<http://127.0.0.1:8007/intro/>

HTTP/2 200 возвращает JSON ответ.

## API сервера

[Документация API](https://resource.intera.space/api/v1/schema/swagger-ui/)

## План разработки микросервиса

1. [Основной план](ROADMAP.md)
