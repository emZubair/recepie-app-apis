from django.urls import path, include
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TagViewSet


router = DefaultRouter()
router.register('tags', TagViewSet)

app_name = 'recepie'

urlpatterns = [
    path('', include(router.urls))
]
