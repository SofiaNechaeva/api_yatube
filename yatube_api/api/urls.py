"""yatube_api/urls."""

from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from api.views import PostViewSet, GroupViewSet, CommentViewSet

router_p_v1 = SimpleRouter()
router_p_v1.register('posts', PostViewSet, basename='posts')

router_g_v1 = SimpleRouter()
router_g_v1.register('groups', GroupViewSet, basename='groups')

router_c_v1 = SimpleRouter()
router_c_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='post-comments',
)

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router_p_v1.urls)),
    path('v1/', include(router_g_v1.urls)),
    path('v1/', include(router_c_v1.urls)),
]
