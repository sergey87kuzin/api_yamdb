from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Comment, Review, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User
        extra_kwargs = {
            'password': {'write_only': True},
            'confirmation_code': {'write_only': True}
        }


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
