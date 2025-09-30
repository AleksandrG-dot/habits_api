from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователей"""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone",
            "city",
            "avatar",
            "password",  # без этого поля не передается пароль в UsersCreateAPIView
            "telegram_chat_id",
        )
