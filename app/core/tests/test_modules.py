"""Test cases for Core app"""

from django.test import TestCase
from django.contrib.auth import get_user_model


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
