from django.urls import path, include
from rest_framework import routers

# router_v1 = routers.DefaultRouter()
# router_v1.register(r'posts', PostViewSet, basename='Post')
# router_v1.register(
#     r'posts/(?P<post_id>\d+)/comments',
#     CommentViewSet, basename='comments'
# )
# router_v1.register('group', GroupViewSet, basename='Group')
# router_v1.register('follow', FollowViewSet, basename='Follow')
#
# api_v1_patterns = [
#     path('', include(router_v1.urls)),
#     path('api-auth/', include('rest_framework.urls'))
# ]
#
# urlpatterns = [
#     path('v1/', include(api_v1_patterns))
# ]