# Менеджер задач (Python)

[![hexlet-check](https://github.com/kicha3007-boop/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/kicha3007-boop/python-project-52/actions)
[![Python CI](https://github.com/kicha3007-boop/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/kicha3007-boop/python-project-52/actions/workflows/pyci.yml)

Task Manager — система управления задачами в духе Redmine: задачи со статусами, исполнителями и
метками, фильтр списка задач, регистрация и вход. Гость видит только главную страницу и список
пользователей.

## Стек

Python, Django, django-filter, PostgreSQL / SQLite, Tailwind CSS (django-tailwind-cli),
whitenoise, gunicorn, Sentry SDK (совместим с Bugsink).

## Установка и запуск

```bash
git clone https://github.com/kicha3007-boop/python-project-52.git
cd python-project-52
cp .env.example .env   # заполнить переменные
make setup             # зависимости, сборка CSS, collectstatic, миграции
make dev               # разработка: runserver + пересборка стилей
make start             # продакшен (gunicorn), http://localhost:8000
```

Переменные окружения:

- `SECRET_KEY` — секрет Django
- `DATABASE_URL` — строка подключения к PostgreSQL; без неё используется SQLite (`db.sqlite3`)
- `DEBUG` — `true` для отладки, в продакшене не задаётся
- `SENTRY_DSN` — DSN коллектора ошибок (Bugsink или Sentry), необязательно

Деплой на render.com: команда сборки `make build`, запуска — `make render-start`.

## Разработка

```bash
make lint            # ruff
make test            # тесты
make test-coverage   # тесты с порогом покрытия из pyproject.toml
```

## Устройство

- `task_manager/users`, `statuses`, `labels`, `tasks` — приложения сущностей: модели, формы, представления, маршруты, тесты.
- `task_manager/mixins.py` — общие правила доступа: вход обязателен, правка только своей записи, защита связанных записей от удаления.
- `task_manager/tasks/filters.py` — фильтр задач по статусу, исполнителю, метке и автору.
- `task_manager/templates/` — базовый шаблон, общие формы и подтверждение удаления, компоненты.

---

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>
