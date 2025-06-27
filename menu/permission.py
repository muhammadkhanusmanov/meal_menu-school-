from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role_id', None) == 1

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role_id', None) == 5

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role_id', None) == 2

class IsParent(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role_id', None) == 3
