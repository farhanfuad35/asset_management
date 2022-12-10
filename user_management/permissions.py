from rest_framework import permissions


class IsCompanyAdmin(permissions.BasePermission):
    """
    Return True if the user is a company admin
    """

    def has_permission(self, request, view):
        if request.user is None or request.user.employee is None:
            return False
        employee = request.user.employee
        return employee.is_company_admin


class IsEmployee(permissions.BasePermission):
    """
    Return True if the user is an employee (or company admin)
    """

    def has_permission(self, request, view):
        if request.user is None or request.user.employee is None:
            return False
        return True


class IsSoftwareAdmin(permissions.BasePermission):
    """
    Returns True if the user is a staff (django user.is_stuff)
    """

    def has_permission(self, request, view):
        if request.user is None:
            return False

        return request.user.is_stuff or request.user.is_superuser
