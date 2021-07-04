"""Test cases for Core app"""

from django.db import models
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Tag, Ingredient, Recepie


def sample_user(email='test@example.com', password='admin12345'):
    """Create a sample user"""

    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):
    """User model Test cases"""

    def test_user_creation_with_email_successfull(self):
        """Test user creation with email is successfull"""

        email = "test@example.com"
        password = "admin12345"

        user = get_user_model().objects.create_user(
            email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_is_normalized(self):
        """ Test that user email is normalized when created """

        email = "test@EXAMPLe.COM"

        user = get_user_model().objects.create_user(email, 'admin12345')

        self.assertEqual(user.email, email.lower())

    def test_invalid_email_error(self):
        """Test creating a user with invliad Email"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "admin12345")

    def test_create_super_user(self):
        """ Test creating a super user """

        user = get_user_model().objects.create_superuser(
            'test@example.com', 'admin12345'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test tag's string representation"""

        tag = Tag.objects.create(
            user=sample_user(), name='vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """Test ingredients's string representation"""

        ingred = Ingredient.objects.create(
            user=sample_user(), name='Cucumber'
        )

        self.assertEqual(str(ingred), ingred.name)

    def test_recepie_str(self):
        """Test string representation of Recepie"""

        recepie = Recepie.objects.create(
            title='Tikka Biryani',
            user=sample_user(),
            minutes_to_deliver=30,
            price=250
        )

        self.assertEqual(str(recepie), recepie.title)
