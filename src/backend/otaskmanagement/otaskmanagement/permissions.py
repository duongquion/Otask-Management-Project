from rest_framework.permissions import SAFE_METHODS, BasePermission
from users.permissions import has_user_permission


class CheckAPIPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            return False

        user = request.user

        if not hasattr(view, "get_project"):
            return True

        project = view.get_project()
        permission = view.required_permission

        return has_user_permission(user, project, permission)
