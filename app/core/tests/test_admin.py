"""Admin site test cases"""

from django.test import TestCase, client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    """Admin side test class"""

    def setUp(self) -> None:
        self.client = client.Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com', password='admin12345', name='Admin'
        )
        self.client.force_login(self.admin_user)
        self.common_user = get_user_model().objects.create_user(
            email='test@example.com', password='admin12345', name='Test'
        )
        return super().setUp()

    def test_user_listing(self):
        """ test that users are listed in admin panel """

        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)
        self.assertContains(response, self.common_user.email)
        self.assertContains(response, self.common_user.name)

    def test_user_change_page(self):
        """ test user chagne page works """

        url = reverse('admin:core_user_change', args=[self.common_user.id])
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)

    def test_create_user_page_works(self):
        """ test new user create page works """

        url = reverse('admin:core_user_add')

        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)
