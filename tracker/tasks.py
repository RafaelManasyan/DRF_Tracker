import logging
from datetime import timedelta, datetime
from celery import shared_task
from django.utils.timezone import now, localtime, get_current_timezone, make_aware

from tracker.models import Habit
from tracker.services import send_tg_message

logger = logging.getLogger(__name__)


@shared_task
def schedule_habit_notifications():
    logger.info("Запуск schedule_habit_notifications")
    habits = Habit.objects.filter(creator__notificator_is_on=True)
    current_time = localtime()
    today = current_time.date()

    for habit in habits:
        if habit.last_notified:
            days_since = (today - habit.last_notified).days
        else:
            days_since = habit.period

        if days_since >= habit.period:
            scheduled_time = datetime.combine(today, habit.time)
            scheduled_time = make_aware(scheduled_time, get_current_timezone())
            if scheduled_time < current_time:
                scheduled_time += timedelta(days=1)
            delay = (scheduled_time - current_time).total_seconds()
            send_habit_notification.apply_async((habit.id,), countdown=delay)


@shared_task
def send_habit_notification(habit_id):
    logger.info(f"Запуск send_habit_notification для habit_id={habit_id}")
    habit = Habit.objects.get(id=habit_id)
    user = habit.creator
    message = str(habit)
    if user.tg_chat_id:
        send_tg_message(user.tg_chat_id, message)
        habit.last_notified = now().date()
        habit.save()
