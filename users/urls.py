from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.views import (UsersCreateAPIView, UsersDestroyApiView,
                         UsersRetrieveApiView, UsersUpdateApiView)

urlpatterns = [
    path("register/", UsersCreateAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("<int:pk>/", UsersRetrieveApiView.as_view(), name="user"),
    path("<int:pk>/update/", UsersUpdateApiView.as_view(), name="users_update"),
    path("<int:pk>/delete/", UsersDestroyApiView.as_view(), name="users_delete"),
]
