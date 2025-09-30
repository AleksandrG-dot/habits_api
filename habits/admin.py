from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "action",
        "time",
        "place",
        "is_pleasant",
        "is_public",
        "created_at",
    )
    list_filter = ("is_pleasant", "is_public", "created_at")
    search_fields = ("action", "place", "user__email")
    readonly_fields = ("created_at",)
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "user",
                    "action",
                    "place",
                    "time",
                    "periodicity",
                )
            },
        ),
        (
            "Характеристики привычки",
            {
                "fields": (
                    "is_pleasant",
                    "is_public",
                    "reward",
                    "related_habit",
                    "time_required",
                    "created_at",
                )
            },
        ),
    )
