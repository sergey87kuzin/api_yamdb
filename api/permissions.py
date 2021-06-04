from rest_framework import permissions


class ReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'admin'

