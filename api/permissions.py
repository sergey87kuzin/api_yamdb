from rest_framework import permissions

AUTHOR_METHODS = ('GET', 'PATCH')


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'a'
