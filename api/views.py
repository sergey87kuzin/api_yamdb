
from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, status  # mixins
from .serializers import UserSerializer
from .models import User
from .permissions import AdminPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework_jwt.settings import api_settings

def make_random_password(self):
    return get_random_string(length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '123456789')

@api_view(['POST'])
def send_mail(self):
    email = self.data.get('email')
    # if self.user.confirmation_code:
    #     code=self.user.confirmation_code
    #     send_mail('Your code', f'your confirmation code is {code}',
    #     'gbgtwvkby@example.com', [email], fail_silently=False)
    #     return code
    code = make_random_password(self)
    user = User.objects.create_user(email=email)
    user.password = code
    # send_mail('Your code', f'your confirmation code is {code}',
    #           'gbgtwvkby@example.com', [email], fail_silently=False)
    return Response(code, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def make_token(self):
    email = self.data.get('email')
    code = self.data.get('confirmation_code')
    user = User.objects.get(email=email, password=code)
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return Response(token, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['GET', 'PATCH'])
def profile(request, **kwargs):
    if request.user.is_authenticated:
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
    return Response(status=status.HTTP_401_UNAUTHORIZED)
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
