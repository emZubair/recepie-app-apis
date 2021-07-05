from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import serializers, status
from rest_framework.test import APIClient

from core.models import Recepie, Tag, Ingredient
from recepie.serializers import RecepieSerializer, RecepieDetailSerializer


RECEPIE_URL = reverse('recepie:recepie-list')


def detail_url(recepie_id):
    """Create a recepie URL"""

    return reverse('recepie:recepie-detail', args=[recepie_id])


def sample_tag(user, name='Main Tag'):
    """Create a sample Tag"""

    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Main Ingredient'):
    """Create and return a sample Ingredients"""

    return Ingredient.objects.create(user=user, name=name)


def sample_recepie(user, **params):
    """Create and return sample Recepie"""

    defaults = {'title': 'Sample Recepie',
                'minutes_to_deliver': 30, 'price': 35.6}
    defaults.update(params)
    return Recepie.objects.create(user=user, **defaults)


class PublicRecepieAPITests(TestCase):
    """Test recepie public APIs"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_authentication_is_required(self):
        """Test authentication is required to access recepie list"""

        response = self.client.get(RECEPIE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecepieAPITests(TestCase):
    """Test private APIs"""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email='test@example.com', password='admin12345')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_recepie_list(self):
        """Test list of recepies retrival is successful """

        sample_recepie(self.user, title='Test recepie one')
        sample_recepie(self.user)

        response = self.client.get(RECEPIE_URL)
        recepies = Recepie.objects.all().order_by('-id')
        serializer = RecepieSerializer(recepies, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_recepies_limited_to_user(self):
        """Test user can retrieve only their recepies """

        sample_recepie(self.user)
        user_2 = get_user_model().objects.create_user(
            'admin@example.com', password='admin12134')
        sample_recepie(user_2)

        res = self.client.get(RECEPIE_URL)
        recepies = Recepie.objects.filter(user=self.user)
        serializer = RecepieSerializer(recepies, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recepie_detail(self):
        """Test viewing a recepie details"""
        recepie = sample_recepie(self.user)
        recepie.tags.add(sample_tag(self.user))
        recepie.ingredients.add(sample_ingredient(self.user))

        url = detail_url(recepie.id)
        response = self.client.get(url)
        serializer = RecepieDetailSerializer(recepie)
        self.assertEqual(response.data, serializer.data)
