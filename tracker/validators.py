from datetime import timedelta

from django.core.exceptions import ValidationError


def fee_or_habit_validator(instance):
    if instance.fee and instance.associated_habit:
        raise ValidationError("Нельзя одновременно указывать связанную привычку и вознаграждение!"
                              "Заполните только одно из этих полей!")


def max_time_validator(value):
    if value > timedelta(seconds=120):
        raise ValidationError("Время выполнения не может быть больше 120 секунд, исправьте поле времени!")


def enjoyable_associated_habit(instance):
    associated_habit = instance.associated_habit
    if associated_habit and not associated_habit.is_enjoyable:
        raise ValidationError("Связанная привычка должна быть приятной!")


def fee_habit_validator_for_enjoyable_habit(instance):
    errors = {}
    if instance.is_enjoyable:
        if instance.fee:
            errors['fee'] = "Приятная привычка не должна иметь вознаграждения!"
        if instance.associated_habit:
            errors['associated_habit'] = "Приятная привычка не должна иметь связанной привычки!"
    if errors:
        raise ValidationError(errors)


def habit_period_validator(value):
    if value > timedelta(days=7):
        raise ValidationError("Привычка должна выполняться не реже одного раза в неделю!")
