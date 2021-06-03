
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import TitleViewSet, GenreViewSet, CategoryViewSet
from . import views

router_v1 = SimpleRouter()
router_v1.register(r'users', views.UserViewSet, basename='users')
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('v1/users/me/', views.Profile.as_view(
        {'get': 'retrieve', 'patch': 'partial_update'}), name='profile'),
    path('v1/auth/email/', views.sending_mail, name='send_mail'),
    path('v1/auth/token/', views.make_token, name='token'),
    path('v1/', include(api_v1_patterns)),

api_v1_patterns = [
    path('', include(router_v1.urls))
]
