from datetime import timedelta

from django.db import models


class Habit(models.Model):
    creator = models.ForeignKey('User', verbose_name='Создатель', on_delete=models.CASCADE)
    place = models.CharField(max_length=100, verbose_name='Место выполнения')
    time = models.TimeField(verbose_name='Время выполнения')
    action = models.CharField(max_length=250, verbose_name='Действие')
    is_enjoyable = models.BooleanField(verbose_name='Приятность')
    associated_habit = models.ForeignKey('Habit', on_delete=models.SET_NULL, verbose_name='Связанная привычка')
    period = models.DurationField(verbose_name='Периодичность', default=timedelta(days=1))
    fee = models.CharField(verbose_name='Вознаграждение за выполненную привычку')
    action_time = models.DurationField(verbose_name='Время на выполнение')
    is_public = models.BooleanField(verbose_name='Публичность')
