# Установим базовый образ Python 3.12.8 slim и обозначим как builder
FROM python:3.12.8-slim AS builder
ENV PYTHONUNBUFFERED=1

# Установим рабочую директорию
WORKDIR /app

# Установим uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.5.13 /uv /bin/uv

# Установим необходимые переменные среды для uv
# Компиляция байткода
ENV UV_COMPILE_BYTECODE=1
# Режим кэширования
ENV UV_LINK_MODE=copy

# Установим необходимые пакеты для сборки, такие как gcc и зависимости Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Установим зависимости
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
COPY uv.lock pyproject.toml /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Скопируем исходный код проекта
ADD .. /app

# Синхронизируем проект
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable

# Собираем минимальный образ для запуска
FROM python:3.12.8-slim

# Установим рабочую директорию
WORKDIR /app

# Скопируем виртуальное окружение из builder
COPY --from=builder /app/.venv /app/.venv

# Настроим виртуальное окружение как активное
ENV PATH="/app/.venv/bin:$PATH"

# Установим пользователя для запуска приложения
RUN groupadd -r app && useradd -r -g app app
USER app

# Команда для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
