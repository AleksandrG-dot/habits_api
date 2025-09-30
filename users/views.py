from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializer import UserSerializer


class UsersCreateAPIView(generics.CreateAPIView):
    """Дженерик для создания пользователя"""

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(
            serializer.validated_data["password"]
        )  # было user.set_password(user.password)
        user.save()


class UsersRetrieveApiView(generics.RetrieveAPIView):
    """Дженерик для получения пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UsersUpdateApiView(generics.UpdateAPIView):
    """Дженерик для обновления данных пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UsersDestroyApiView(generics.DestroyAPIView):
    """Дженерик для удаления пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
