from django.contrib import admin

from users.models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "phone",
        "city",
        "telegram_chat_id",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active", "city")
    search_fields = ("email", "phone", "city")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Персональная информация",
            {"fields": ("phone", "city", "avatar", "telegram_chat_id")},
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )
