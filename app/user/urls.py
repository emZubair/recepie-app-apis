from django.urls import path

from .views import CreateUserView, CreateTokenView


app_name = "user"


urlpatterns = [
    path('token/', CreateTokenView.as_view(), name='token'),
    path('create/', CreateUserView.as_view(), name='create'),
]
