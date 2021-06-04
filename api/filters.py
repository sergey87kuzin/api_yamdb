from django_filters import rest_framework as filter

from .models import Title


class TitleFilter(filter.FilterSet):
    name = filter.CharFilter(
        field_name='name',
        lookup_expr='contains'
    )
    category = filter.CharFilter(
        field_name='category__slug',
        lookup_expr='contains'
    )
    genre = filter.CharFilter(
        field_name='genre__slug',
        lookup_expr='contains'
    )

    class Meta:
        model = Title
        fields = '__all__'