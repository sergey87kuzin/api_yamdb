from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db.models.aggregates import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .models import Category, Comment, Genre, Review, Title, User
from .permissions import (
    AdminPermission, IsAdminOrReadOnly, OwnerAdminModeratorReadonly,
    SelfMadeAdminPermission,
)
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, ReviewSerializer,
    TitleCreateSerializer, TitleReadSerializer, UserSerializer,
)


@api_view(['POST'])
def sending_mail(self):
    email = self.data.get('email')
    try:
        validate_email(email)
    except ValidationError:
        return Response('invalid email')
    user = User.objects.create_user(email=email)
    code = default_token_generator.make_token(user)
    data = {'username': code, 'confirmation_code': code}
    serializer = UserSerializer(user, data=data,
                                partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    send_mail('Your code', f'your confirmation code is {code}',
              settings.ADMIN_EMAIL, [email, ], fail_silently=False)
    return Response(code)


@api_view(['POST'])
def make_token(self):
    email = self.data.get('email')
    try:
        validate_email(email)
    except ValidationError:
        return Response('invalid email')
    code = self.data.get('confirmation_code')
    user = get_object_or_404(User, email=email, confirmation_code=code)
    try:
        default_token_generator.check_token(user, code)
    except ValidationError:
        return Response('invalid code')
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, AdminPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', ]

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated, SelfMadeAdminPermission])
    def me(self, request):
        instance = request.user
        if request.method == 'GET':
            serializer = UserSerializer(instance)
        elif request.method == 'PATCH':
            serializer = UserSerializer(instance, data=request.data,
                                        partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, OwnerAdminModeratorReadonly,
    )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        reviews = get_object_or_404(Title, id=title_id).reviews.all()
        return reviews

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, OwnerAdminModeratorReadonly,
    )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        comments = get_object_or_404(Review, id=review_id).comments.all()
        return comments

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class CreateListDestroyViewSet(
    DestroyModelMixin, CreateModelMixin,
    ListModelMixin, viewsets.GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    filterset_fields = ['name', 'year', 'category', 'genre']

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return TitleCreateSerializer
        return TitleReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
