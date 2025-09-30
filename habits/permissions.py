from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Право доступа только для владельца объекта."""

    message = "Не владелец"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
