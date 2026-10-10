PORT ?= 8000

setup: install build-css collectstatic migrate

install:
	uv sync

build-css:
	uv run python manage.py tailwind build --force

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

dev:
	uv run python manage.py tailwind runserver

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

lint:
	uv run ruff check task_manager

test:
	uv run python manage.py test

test-coverage:
	uv run coverage run manage.py test
	uv run coverage report
	uv run coverage xml

check: lint test

.PHONY: setup install build-css collectstatic migrate dev start build render-start lint test test-coverage check
