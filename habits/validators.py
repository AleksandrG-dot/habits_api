from rest_framework import serializers


class RewardOrRelatedHabitValidator:
    def __call__(self, attrs):
        related_habit = attrs.get("related_habit")
        reward = attrs.get("reward")

        if related_habit and reward:
            raise serializers.ValidationError(
                "Нельзя одновременно выбирать связанную привычку и вознаграждение."
            )


class TimeRequiredValidator:
    def __call__(self, value):
        if value > 120:
            raise serializers.ValidationError(
                "Время выполнения не может быть больше 120 секунд."
            )


class RelatedHabitIsPleasantValidator:
    def __call__(self, value):
        if value and not value.is_pleasant:
            raise serializers.ValidationError(
                "В связанные привычки могут попадать только привычки с признаком приятной привычки."
            )


class PleasantHabitNoRewardValidator:
    def __call__(self, attrs):
        is_pleasant = attrs.get("is_pleasant")
        related_habit = attrs.get("related_habit")
        reward = attrs.get("reward")

        if is_pleasant:
            if reward or related_habit:
                raise serializers.ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )


class PeriodicityValidator:
    def __call__(self, value):
        if value < 1 or value > 7:
            raise serializers.ValidationError(
                "Периодичность должна быть от 1 до 7 дней."
            )
