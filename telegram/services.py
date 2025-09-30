import requests

from config.settings import TELEGRAM_TOKEN


def create_reminder_message(habit):
    """Создание текста напоминания для привычки."""
    reward_text = ""

    if habit.reward:
        reward_text = f"\n\n🎁 Вознаграждение: {habit.reward}"
    elif habit.related_habit:
        reward_text = f"\n\n🎁 После этого: {habit.related_habit.action}"

    message = (
        f"🔔 <b>Напоминание о привычке</b>\n\n"
        f"📍 Место: {habit.place}\n"
        f"⏰ Время: {habit.time.strftime('%H:%M')}\n"
        f"📝 Действие: {habit.action}\n"
        f"⏱️ Время на выполнение: {habit.time_required} сек.{reward_text}"
    )

    return message


def send_telegram_message(text: str, chat_id: str) -> bool:
    """
    Отправка сообщения через Telegram бота.

    text: Текст сообщения
    chat_id: ID чата пользователя
    :return: True если успешно, False если ошибка
    """
    token = TELEGRAM_TOKEN
    if not token:
        print("TELEGRAM_TOKEN не установлен")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")
        return False
