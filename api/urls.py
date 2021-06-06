from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router_v1 = SimpleRouter()
router_v1.register('titles', views.TitleViewSet, basename='title')
router_v1.register('categories', views.CategoryViewSet, basename='category')
router_v1.register('genres', views.GenreViewSet, basename='genre')

api_v1_patterns = [
    path('', include(router_v1.urls))
]

urlpatterns = [
    path('v1/', include(api_v1_patterns)),
]