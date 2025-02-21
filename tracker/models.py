from datetime import timedelta

from django.db import models

from config import settings


class Habit(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Создатель", on_delete=models.CASCADE
    )
    place = models.CharField(max_length=100, verbose_name="Место выполнения")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=250, verbose_name="Действие")
    is_enjoyable = models.BooleanField(verbose_name="Приятность", default=False)
    associated_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        null=True,
        blank=True,
    )
    period = models.PositiveIntegerField(
        verbose_name="Периодичность (в днях)", default=1
    )
    fee = models.CharField(
        verbose_name="Вознаграждение за выполненную привычку", null=True, blank=True
    )
    action_time = models.DurationField(
        verbose_name="Время на выполнение", default=timedelta(seconds=120)
    )
    is_public = models.BooleanField(verbose_name="Публичность")
    last_notified = models.DateField(
        verbose_name="Время последнего уведомления", null=True, blank=True
    )

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"
