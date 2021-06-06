from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_admin
                or request.method in permissions.SAFE_METHODS
            )
        return request.method in permissions.SAFE_METHODS


class OwnerAdminModeratorReadonly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.is_not_user
                or request.method in permissions.SAFE_METHODS
                or obj.author == request.user
            )
        return request.method in permissions.SAFE_METHODS


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_admin


class SelfMadeAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_not_user:
            return not request.data.get('role')
        return True
