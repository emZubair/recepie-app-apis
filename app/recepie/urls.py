from django.urls import path, include
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, IngredientViewSet


router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredient', IngredientViewSet)

app_name = 'recepie'

urlpatterns = [
    path('', include(router.urls))
]
