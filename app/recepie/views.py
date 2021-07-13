
from os import path
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recepie
from .serializers import (RecepieDetailSerializer, TagSerializer, IngredientSerializer, RecepieSerializer,
                          RecepieImageSerializer)


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

    def _parse_tags_to_int(self, qs):
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Receive Recepies related to authenticated user"""

        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredient')
        queryset = self.queryset
        if tags:
            queryset.filter(tags__id__in=self._parse_tags_to_int(tags))
        if ingredients:
            queryset.filter(
                ingredients__id__in=self._parse_tags_to_int(ingredients))
        return queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self, *args, **kwargs):
        """Return appropiate serializer class """

        if self.action == 'retrieve':
            return RecepieDetailSerializer
        elif self.action == 'image_upload':
            return RecepieImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='image-upload')
    def image_upload(self, request, pk=None):
        """ Upload an image to Receipe """

        recepie = self.get_object()
        serializer = self.get_serializer(recepie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
