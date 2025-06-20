from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(
    r'users',
    views.UserCreateViewSet,
    basename='user_create',
)
router.register(
    r'users',
    views.UserProfileViewSet,
    basename='user_profile',
)
router.register(
    r'users',
    views.AvatarViewSet,
    basename='user_avatar',
)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'users/set_password/',
        views.NewPasswordViewSet.as_view(
            {
                'post': 'set_password',
            }
        ),
    ),
    path('', include(router.urls)),
]
