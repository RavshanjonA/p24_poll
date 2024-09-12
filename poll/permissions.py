from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOrReadonlyAuthentication(permissions.BasePermission):
    message = "creating vote for only admins."

    def has_permission(self, request, view):
        if (
            request.method in permissions.SAFE_METHODS
            and request.user.is_authenticated
            and not request.user.is_staff
        ):
            return True
        elif request.user.is_authenticated and request.user.is_staff:
            return True
        return False
