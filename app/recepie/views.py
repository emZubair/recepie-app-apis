
from rest_framework import serializers, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recepie
from .serializers import RecepieDetailSerializer, TagSerializer, IngredientSerializer, RecepieSerializer


class BaseRecipieAttributes(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base class for recepies and ingreidents"""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipieAttributes):
    """Manage tags in the DB"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseRecipieAttributes):
    """Manage ingredients inthe DB"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecepieViewSet(viewsets.ModelViewSet):
    """Manage recepies"""

    queryset = Recepie.objects.all()
    serializer_class = RecepieSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        """Receive Recepies related to authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self, *args, **kwargs):
        """Return appropiate serializer class """
        if self.action == 'retrieve':
            return RecepieDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
