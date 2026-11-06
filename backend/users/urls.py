from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(
    r'users',
    views.UserCreateViewSet,
    basename='user-create', 
)
router.register(
    r'users',
    views.UserProfileViewSet,
    basename='user-profile',
)
router.register(
    r'users',
    views.AvatarViewSet,
    basename='user-avatar',
)

useralbums_router = DefaultRouter()
useralbums_router.register(
    r'users',
    views.UserListsViewSet,
    basename='user-albums-list',
)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'search/',
        views.SearchViewSet.as_view({
            'get': 'search',
        })
    ),
    path(
        'users/set_password/',
        views.NewPasswordViewSet.as_view(
            {
                'post': 'set_password',
            }
        ),
        name="user-set-password",
    ),
    path('', include(useralbums_router.urls)),
    path('', include(router.urls)),
]
