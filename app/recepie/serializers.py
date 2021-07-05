
from django.db import models
from django.db.models import fields
from rest_framework import serializers

from core.models import Tag, Ingredient, Recepie


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredients"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecepieSerializer(serializers.ModelSerializer):
    """Serializer for Recepie """

    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingredient.objects.all())

    class Meta:
        model = Recepie
        fields = ('id', 'title', 'user', 'price',
                  'minutes_to_deliver', 'link', 'tags', 'ingredients')

        read_only_fields = ('id',)


class RecepieDetailSerializer(RecepieSerializer):
    """ Serializer for recepie detail """

    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
