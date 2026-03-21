from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import (
    ReviewModelViewSet,
    ReviewCommentViewSet,
)


router = DefaultRouter()
router.register(
    r'reviews',
    ReviewModelViewSet,
    basename='review'
)
router.register(
    r'comments',
    ReviewCommentViewSet,
    basename='review_comments',
)

urlpatterns = [
    path('', include(router.urls)),
]
