""" User APIs tests """

from django import urls
from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient


ME = reverse('user:me')
TOKEN_URL = reverse('user:token')
CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Create user with given params"""
    return get_user_model().objects.create_user(**params)


# class PublicUserAPITests(TestCase):
#     """ Tests for Public User APIs """

#     def setUp(self) -> None:
#         self.client = APIClient()

#     def test_create_valid_user_success(self):
#         """Test user creation with valid payload is successful"""

#         payload = {'email': 'test@example.com',
#                    'password': 'admin12345', 'name': 'Tester User'}

#         response = self.client.post(CREATE_USER_URL, payload)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         user = get_user_model().objects.get(**response.data)
#         self.assertTrue(user.check_password(payload['password']))
#         self.assertNotIn('password', response.data)

#     def test_user_exists(self):
#         """ Test user that already exists fails """

#         payload = {'email': 'test@example.com',
#                    'password': 'admin12345', 'name': 'Tester User'}

#         create_user(**payload)
#         response = self.client.post(CREATE_USER_URL, payload)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_password_too_short(self):
#         """ Test password should be more than 5 characters """

#         payload = {'email': 'test@example.com',
#                    'password': 'pw', 'name': 'Tester User'}

#         response = self.client.post(CREATE_USER_URL, payload)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         user_exists = get_user_model().objects.filter(
#             email=payload['email']).exists()
#         self.assertFalse(user_exists)

#     def test_create_token_for_user(self):
#         """Test token is created for user"""

#         payload = {'email': 'test@example.com',
#                    'password': 'admin12345'}

#         create_user(**payload)

#         response = self.client.post(TOKEN_URL, payload)
#         self.assertIn('token', response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_create_token_with_invalid_credentials(self):
#         """Test token is not created when for invalid credentials"""

#         create_user(**{'email': 'test@example.com', 'password': 'admin12345'})
#         payload = {'email': 'test@example.com',
#                    'password': 'pw'}

#         response = self.client.post(TOKEN_URL, payload)
#         self.assertNotIn('token', response.data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_create_token_no_user(self):
#         """Test token is not created when user is not registered"""

#         payload = {'email': 'test@example.com', 'password': 'admin12345'}
#         response = self.client.post(TOKEN_URL, payload)

#         self.assertNotIn('token', response.data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_create_token_missing_field(self):
#         """Test Email and password are required Fields"""

#         response = self.client.post(
#             TOKEN_URL, {'email': 'test@example.com', 'password': ''})
#         self.assertNotIn('token', response.data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_retrieve_user_un_authorized(self):
#         """Test that authentication is required for Users"""

#         response = self.client.get(ME)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PriavteUserAPITests(TestCase):
    """ Test cases to validate login required to access the following endpoints """

    def setUp(self) -> None:
        self.user = create_user(email='test@example.com',
                                password='admin12345', name='Test User')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_successfull(self):
        """Test authenticated user can access profile"""

        response = self.client.get(ME)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'name': self.user.name, 'email': self.user.email})

    def test_post_not_allowed(self):
        """Test post method not allowed"""

        response = self.client.post(ME, {})

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_update(self):
        """Test updating user profile for authenticate users"""

        payload = {'name': 'Taimorr', 'password': 'admin123456'}

        response = self.client.patch(ME, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload.get('name'))
        self.assertTrue(self.user.check_password(payload.get('password')))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
