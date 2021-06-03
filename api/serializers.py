from rest_framework import serializers

from .models import User, Title, Genre, Category


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User
        extra_kwargs = {
            'password': {'write_only': True}
        }


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'
