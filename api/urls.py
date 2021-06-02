from django.urls import path, include
from rest_framework import routers

from .views import TitleViewSet, GenreViewSet, CategoryViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')

api_v1_patterns = [
    path('', include(router_v1.urls))
]

urlpatterns = [
    path('v1/', include(api_v1_patterns))
]
