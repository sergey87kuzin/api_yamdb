from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == 'admin'
                or request.method in permissions.SAFE_METHODS
            )
        return request.method in permissions.SAFE_METHODS


class OwnerAdminModeratorReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.role in ['moderator', 'admin']
                or request.method in permissions.SAFE_METHODS
                or obj.author == request.user
            )
        return request.method in permissions.SAFE_METHODS


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'admin'


class SelfMadeAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role != 'admin':
            return not request.data.get('role')
        return True
