from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import ReviewModelViewSet


router = DefaultRouter()
router.register(
    r'reviews',
    ReviewModelViewSet,
    basename='review'
)

urlpatterns = [
    path('', include(router.urls)),
]
