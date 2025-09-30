from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginations import HabitPagination
from habits.permissions import IsOwner
from habits.serializers import (HabitCreateSerializer, HabitListSerializer,
                                HabitSerializer)


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с привычками."""

    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Установка пользователя владельцем привычки"""
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """Расстановка прав доступа на запросы."""
        if self.action == "list_public":
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy", "retrieve", "list"]:
            return [IsAuthenticated(), IsOwner()]
        return super().get_permissions()

    def get_queryset(self):
        """Возвращает привычки пользователя или список публичных привычек."""
        user = self.request.user
        if self.action == "list_public":
            return Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=user)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия."""
        if self.action == "create":
            return HabitCreateSerializer
        elif self.action in ["list", "retrieve"]:
            return HabitListSerializer
        return HabitSerializer

    def list_public(self, request, *args, **kwargs):
        """Список публичных привычек."""
        return self.list(request, *args, **kwargs)
