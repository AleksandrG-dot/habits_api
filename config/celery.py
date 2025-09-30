import os

from celery import Celery
from celery.schedules import crontab

from config.settings import CELERY_TIME_INTERVAL

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check-habits-every-n-minutes": {
        "task": "telegram.tasks.check_habits_and_send_reminders",
        "schedule": crontab(
            minute=f"*/{CELERY_TIME_INTERVAL}"
        ),  # Запуск задачи каждые n минут
    },
}
