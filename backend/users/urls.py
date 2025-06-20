from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserCreateListViewSet


router = DefaultRouter()

router.register(
    r'users',
    UserCreateListViewSet,
    basename='user_list_create',
)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
