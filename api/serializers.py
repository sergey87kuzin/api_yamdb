from django.db.models.aggregates import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleCreateSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )

    class Meta:
        exclude = ('author',)
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = Title.objects.annotate(
            title_rate=Avg('reviews__score')
        ).filter(id=obj.id).first()
        return rating.title_rate

    class Meta:
        exclude = ('author',)
        model = Title