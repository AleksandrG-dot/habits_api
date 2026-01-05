FROM python:3.11-slim

WORKDIR /app

# Временные переменные по умолчанию (нужны для сборки образа в build):
ENV SECRET_KEY=temp-build-key
ENV TELEGRAM_TOKEN=temp-token
ENV DEBUG=True
ENV DATABASE_NAME=temp_db
ENV DATABASE_USER=temp_user
ENV DATABASE_PASSWORD=temp_pass
ENV DATABASE_HOST=localhost
ENV DATABASE_PORT=5432
ENV CELERY_BROKER_URL=redis://redis:6379/0
ENV CELERY_RESULT_BACKEND=redis://redis:6379/0
ENV ALLOWED_HOSTS=localhost,127.0.0.1
ENV CORS_ALLOWED_ORIGINS=http://localhost:3000
ENV CSRF_TRUSTED_ORIGINS=http://localhost

# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements и установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Создаем и даем права на директорию для статических и медиа файлов
RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles
RUN mkdir -p /app/media && chmod -R 755 /app/media

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
