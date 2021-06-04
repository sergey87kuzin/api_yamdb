from rest_framework import viewsets, mixins, filters, pagination

from . import serializers
from . import permissions
from .models import Title, Genre, Category
from .filters import TitleFilter


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer
    permission_classes = [
        permissions.ReadOnly | permissions.AdminPermission
    ]
    filterset_class = TitleFilter
    pagination_class = pagination.PageNumberPagination


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [
        permissions.ReadOnly | permissions.AdminPermission
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    pagination_class = pagination.PageNumberPagination


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [
        permissions.ReadOnly | permissions.AdminPermission
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    pagination_class = pagination.PageNumberPagination