from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from config.settings import CELERY_TIME_INTERVAL
from habits.models import Habit
from telegram.services import create_reminder_message, send_telegram_message


@shared_task
def check_habits_and_send_reminders():
    """
    Задача для проверки привычек и отправки напоминаний.
    Запускается каждые CELERY_TIME_INTERVAL минут.
    """
    # Получаем текущее время
    now = timezone.now()
    current_time = now.time()
    # Вычисляем время n минут вперед
    n_minutes_ahead = now + relativedelta(minutes=CELERY_TIME_INTERVAL)
    n_minutes_ahead = n_minutes_ahead.time()

    # Получаем привычки, которые нужно выполнить в текущее время
    habits_to_remind = Habit.objects.filter(
        time__range=(current_time, n_minutes_ahead)
    ).select_related("user")

    for habit in habits_to_remind:
        if habit.user.telegram_chat_id:
            message = create_reminder_message(habit)
            send_telegram_message(message, habit.user.telegram_chat_id)

    return f"В {current_time} проверено {habits_to_remind.count()} привычек"
