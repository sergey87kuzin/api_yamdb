from rest_framework import permissions


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'admin'
