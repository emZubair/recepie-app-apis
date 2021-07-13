from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient, Recepie
from recepie.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recepie:ingredient-list')


class PublicIngredientsAPITest(TestCase):
    """Test public ingredient APIs"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """Test login is required"""

        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITest(TestCase):
    """Test Private APIs"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com', password='admin12345')
        self.client.force_authenticate(self.user)

    def test_ingrident_list(self):
        """Test retriving Ingreident list"""

        Ingredient.objects.create(user=self.user, name='Salt')
        Ingredient.objects.create(user=self.user, name='Capcicum')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)

    def test_ingredients_limited_to_current_user(self):
        """Test user can only access their ingredients"""

        user_2 = get_user_model().objects.create_user(
            email='admin@example.com', password='admin12345')

        Ingredient.objects.create(user=user_2, name='Salt')
        ingred = Ingredient.objects.create(user=self.user, name='Capcicum')

        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0].get('name'), ingred.name)

    def test_create_ingredent_successful(self):
        """Test ingredient is created successfull"""

        payload = {'name': 'Cabbage'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user, name=payload.get('name')).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test ingredient with invalid data is not crated"""

        res = self.client.post(INGREDIENTS_URL, {'name': ''})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ingredients_assigned_to_recepie(self):
        """Test only those ingredients are returned assigned to recepie"""

        ingredient1 = Ingredient.objects.create(user=self.user, name='Chicken')
        ingredient2 = Ingredient.objects.create(user=self.user, name='Fish')

        recepie = Recepie.objects.create(
            title='Chicken Biryani', minutes_to_deliver=45, price=300, user=self.user)

        recepie.ingredients.add(ingredient1)

        response = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        serializer1 = IngredientSerializer(ingredient1)
        serializer2 = IngredientSerializer(ingredient2)

        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_ingredients_filter_unique(self):
        """Test unique ingredients are assigned"""

        ingredient1 = Ingredient.objects.create(user=self.user, name='Chicken')
        Ingredient.objects.create(user=self.user, name='Fish')

        recepie = Recepie.objects.create(
            title='Chicken Biryani', minutes_to_deliver=45, price=300, user=self.user)

        recepie.ingredients.add(ingredient1)

        recepie2 = Recepie.objects.create(
            title='Fish Kabab', minutes_to_deliver=45, price=300, user=self.user)

        recepie2.ingredients.add(ingredient1)

        response = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})
        self.assertEqual(len(response.data), 1)
