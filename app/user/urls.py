from django.urls import path

from .views import CreateUserView, CreateTokenView, ManageUserView


app_name = "user"


urlpatterns = [
    path('me/', ManageUserView.as_view(), name='me'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('create/', CreateUserView.as_view(), name='create'),
]
