from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router_v1 = SimpleRouter()
router_v1.register(r'users', views.UserViewSet, basename='users')


urlpatterns = [
    path('api/v1/users/me/', views.Profile.as_view(
        {'get': 'retrieve', 'patch': 'partial_update'}), name='profile'),
    path('api/v1/auth/email/', views.sending_mail, name='send_mail'),
    path('api/v1/auth/token/', views.make_token, name='token'),
    path('api/v1/', include(router_v1.urls)),
]
