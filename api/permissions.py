from rest_framework import permissions


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'admin'


class SelfMadeAdminPermission(permissions.BasePermission):

    def has_permissions(self, request, view):
        if request.user.role != 'admin':
            return not request.data.get('role')
        return True
