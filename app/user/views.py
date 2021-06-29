"""User API views"""
from rest_framework import generics, serializers
from .serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the sytem"""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """ Create a new token for user """

    serializers = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
