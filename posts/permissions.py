"""Permission for Post application."""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """A permission that checks if user is an owner."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_id == request.user
