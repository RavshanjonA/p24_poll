from rest_framework.permissions import BasePermission


class ActionBasedPermission(BasePermission):
    message = """Sizda bu obyekt va metod uchun permission mavjud emas"""

    def has_permission(self, request, view):

        methods = {
            "GET": 'view',
            "POST": 'add',
            "PATCH": 'change',
            "PUT": 'change',
            "DELETE": 'delete',
        }
        permission_method = methods[request.method]
        codename = f"{permission_method}_{view.basename}"
        permission = request.user.user_permissions.filter(codename=codename)
        if permission:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)


class ExchangePermission(BasePermission):
    message = """Sizda bu obyekt va metod uchun permission mavjud emas"""

    def has_permission(self, request, view):

        methods = {
            "GET": 'view',
            "POST": 'add',
            "PATCH": 'change',
            "PUT": 'change',
            "DELETE": 'delete',
        }
        permission_method = methods[request.method]
        codename = f"{permission_method}_exchange"
        permission = request.user.user_permissions.filter(codename=codename)
        if permission:
            return True
        else:
            return False
