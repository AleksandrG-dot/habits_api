from rest_framework import serializers

from habits.models import Habit
from habits.validators import (PeriodicityValidator,
                               PleasantHabitNoRewardValidator,
                               RelatedHabitIsPleasantValidator,
                               RewardOrRelatedHabitValidator,
                               TimeRequiredValidator)


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели привычки с валидаторами"""

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "time_required",
            "is_public",
            "created_at",
        ]
        read_only_fields = ["user", "created_at"]

    def validate(self, attrs):
        # Валидация связанной привычки и вознаграждения
        RewardOrRelatedHabitValidator()(attrs)

        # Валидация времени выполнения
        if "time_required" in attrs:
            TimeRequiredValidator()(attrs["time_required"])

        # Валидация приятной привычки
        if "is_pleasant" in attrs:
            PleasantHabitNoRewardValidator()(attrs)

        # Валидация связанной привычки (если указана) related_habit=True
        if "related_habit" in attrs and attrs["related_habit"]:
            RelatedHabitIsPleasantValidator()(attrs["related_habit"])

        # Валидация периодичности
        if "periodicity" in attrs:
            PeriodicityValidator()(attrs["periodicity"])

        return attrs


class HabitCreateSerializer(HabitSerializer):
    """Сериализатор для модели привычки для создания привычки"""

    class Meta(HabitSerializer.Meta):
        read_only_fields = ["user", "created_at"]


class HabitListSerializer(HabitSerializer):
    """Сериализатор для модели привычки для отображения списка и 1 записи"""

    class Meta(HabitSerializer.Meta):
        fields = [
            "id",
            "place",
            "time",
            "action",
            "is_pleasant",
            "periodicity",
            "time_required",
            "is_public",
        ]
