from django.core.exceptions import ValidationError
from django.db.models.aggregates import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        fields = '__all__'
        model = User
        extra_kwargs = {
            'password': {'write_only': True},
            'confirmation_code': {'write_only': True}
        }

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Duplicate")
        return lower_email


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        exclude = ('title',)
        model = Review

    def validate(self, data):
        score = data.get('score')
        author = self.context['request'].user
        title_id = self.context['view'].kwargs['title_id']
        if self.context['request'].method == 'POST':
            author_exists = Review.objects.filter(
                author=author, title__id=title_id
            ).exists()
            if author_exists:
                raise ValidationError(
                    'Вы уже оставляли отзыв к данному произведению'
                )
        if score > 10 or score < 1:
            raise ValidationError('Оценка может быть от 1 до 10')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        exclude = ('review',)


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
