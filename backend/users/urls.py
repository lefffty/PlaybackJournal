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

useralbums_router = DefaultRouter()
useralbums_router.register(
    r'users',
    views.UserAlbumsListsViewSet,
    basename='user_albums_list',
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
    path('', include(useralbums_router.urls)),
    path('', include(router.urls)),
]
