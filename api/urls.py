from django.urls import include, path
from . import views
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

router_v1 = SimpleRouter()
router_v1.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('api/v1/users/me/', views.profile, name='profile'),
    path('api/v1/', include(router_v1.urls)),
    path('api/v1/auth/email/', views.send_mail, name='send_mail'),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
