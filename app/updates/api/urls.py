from django.urls import path
from .views import UpdateModelDetailAPI, UpdateModelListAPI


urlpatterns = [
    path('<id>/', UpdateModelDetailAPI.as_view()),
    path('', UpdateModelListAPI.as_view())

]
