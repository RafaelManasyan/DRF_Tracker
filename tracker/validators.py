from datetime import timedelta

from django.core.exceptions import ValidationError


def fee_or_habit_validator(data):
    if data.get("fee") and data.get("associated_habit"):
        raise ValidationError(
            "Нельзя одновременно указывать связанную привычку и вознаграждение!"
            "Заполните только одно из этих полей!"
        )


def max_time_validator(value):
    if value > timedelta(seconds=120):
        raise ValidationError(
            "Время выполнения не может быть больше 120 секунд, исправьте поле времени!"
        )


def enjoyable_associated_habit(data):
    associated_habit = data.get("associated_habit")
    if associated_habit and not associated_habit.is_enjoyable:
        raise ValidationError("Связанная привычка должна быть приятной!")


def fee_habit_validator_for_enjoyable_habit(data):
    if data.get("is_enjoyable"):
        if data.get("fee"):
            raise ValidationError("Приятная привычка не должна иметь вознаграждения")
        if data.get("associated_habit"):
            raise ValidationError(
                "Приятная привычка не должна иметь связанной привычки"
            )
    return data


def habit_period_validator(value):
    if value > 7:
        raise ValidationError(
            "Привычка должна выполняться не реже одного раза в неделю!"
        )
