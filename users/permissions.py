from rest_framework.views import View, Request
from rest_framework import permissions
from users.models import User


class IsEmployeeOrReadOnly(permissions.BasePermission):
    """
    Allows access only to employees.
    """

    # OBS:
    # Request here is the same one from UserView.
    # On this app, if is_superuser == True, then is_employee == True as well.
    def has_permission(self, request: Request, view: View) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_superuser
        )


class IsOwnerOrEmployee(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User) -> bool:
        # if request.user.is_superuser:
        #     return True
        # if request.user == obj:
        #     return True

        return request.user.is_superuser or request.user == obj
