from rest_framework import serializers

from tracker.models import Habit
from tracker.validators import (fee_or_habit_validator, max_time_validator, enjoyable_associated_habit,
                                fee_habit_validator_for_enjoyable_habit, habit_period_validator)


class HabitSerializer(serializers.ModelSerializer):
    action_time = serializers.DurationField(validators=[max_time_validator])
    period = serializers.DurationField(validators=[habit_period_validator])

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [fee_or_habit_validator, enjoyable_associated_habit, fee_habit_validator_for_enjoyable_habit]
