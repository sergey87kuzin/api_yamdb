
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import AdminPermission, SelfMadeAdminPermission
from .serializers import UserSerializer


@api_view(['POST'])
def sending_mail(self):
    email = self.data.get('email')
    user = User.objects.create_user(email=email)
    code = default_token_generator.make_token(user)
    data = {'username': code, 'confirmation_code': code}
    serializer = UserSerializer(user, data=data,
                                partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    send_mail('Your code', f'your confirmation code is {code}',
              'gbgtwvkby@example.com', [email, ], fail_silently=False)
    return Response(code)


@api_view(['POST'])
def make_token(self):
    email = self.data.get('email')
    code = self.data.get('confirmation_code')
    user = User.objects.get(email=email, confirmation_code=code)
    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


class Profile(mixins.RetrieveModelMixin,
              mixins.UpdateModelMixin,
              viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, SelfMadeAdminPermission]

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, AdminPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', ]
