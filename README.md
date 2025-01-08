# Проект с использованием FastAPI, Docker, UV, Alembic, PostgreSQL и Docker Compose

## Установка и настройка

### Установка и настройка UV
1. Создайте виртуальное окружение с использованием Python 3.12.8:
   ```bash
   uv venv --python 3.12.8
   ```
2. Синхронизируйте зависимости из `pyproject.toml` и установите их в виртуальное окружение:
   ```bash
   uv sync
   ```
3. Установка пре-коммит хуков
   ```bash
   uv run pre-commit install
   ```

### Запуск базы данных с помощью Docker Compose
1. Убедитесь, что Docker и Docker Compose установлены на вашей системе.
2. Запустите Docker Compose с конфигурацией базы данных:
   ```bash
   docker-compose up -d
   ```

### Настройка переменных окружения
1. Активируйте переменные окружения из файла `envs/dev.env`:
   ```bash
   set -a
   source envs/dev.env
   set +a
   ```

### Миграции базы данных
1. Создайте новую миграцию для создания таблицы `users`:
   ```bash
   uv run alembic revision --autogenerate -m "create users table"
   ```
2. Примените миграции для обновления базы данных до последней версии:
   ```bash
   uv run alembic upgrade head
   ```

### Запуск приложения
1. Убедитесь, что вы выбрали файл окружения `dev.env` в разделе `paths to .env files`.
2. Запуск дев сервера
   ```bash
   # без релода, в 1 процесс, только веб сервер ювикорна, так легче дебажить
   uv run uvicorn --factory 'app.main:create_application' --log-level='debug' --log-config='uvicorn_logs_config.yaml'
   ```

### Дополнительные команды для миграций
1. Для создания начальной миграции выполните:
   ```bash
   uv run alembic revision --autogenerate -m "initial migration"
   ```

---

## Используемые технологии
- **FastAPI**: веб-фреймворк для разработки REST API.
- **Docker**: контейнеризация приложения.
- **UV**: инструмент для управления виртуальным окружением и зависимостями.
- **Alembic**: инструмент для управления миграциями базы данных.
- **PostgreSQL**: реляционная база данных.
- **Docker Compose**: оркестрация нескольких контейнеров.
