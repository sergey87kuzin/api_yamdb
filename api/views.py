

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets  # mixins,
from .serializers import UserSerializer
from .models import User
from .permissions import AdminPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.pagination import PageNumberPagination


def send_mail(email):
    pass


@api_view(['GET', 'PATCH'])
def profile(request, **kwargs):
    if request.method == 'GET':
        instance = request.user
        serializer = UserSerializer(instance)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        partial = kwargs.pop('partial', True)
        instance = request.user
        serializer = UserSerializer(instance, data=request.data,
                                    partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
# class Profile(mixins.RetrieveModelMixin,
#               mixins.UpdateModelMixin,
#               viewsets.GenericViewSet):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    lookup_value_regex = '[A-Z0-9a-z]+'
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, AdminPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', ]
