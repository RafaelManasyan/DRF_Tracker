import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    'send_habit_reminders_daily': {
        'task': 'tracker.tasks.schedule_habit_notifications',
        'schedule': crontab(minute='*/2'),
    },
}
