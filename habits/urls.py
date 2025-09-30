from django.urls import include, path
from rest_framework.routers import DefaultRouter

from habits.views import HabitViewSet

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habits")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "habits_public/",
        HabitViewSet.as_view({"get": "list_public"}),
        name="habits-public",
    ),
]
