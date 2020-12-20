from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_ADMIN_URL = reverse('admins:create')
TOKEN_URL = reverse('admins:token')

def create_admin(**params):
    return get_user_model().objects.create_user(**params)


class PrivateAdminApiTest(TestCase):
    """Test for the admins api (private - only superusers can create admins)"""

    def setUp(self):
        self.client = APIClient()
    
    def test_create_valid_admin(self):
        """Test creating a admins with valid payloads (json) is successful"""
        payload = {
            'username': 'testuser',
            'name': 'test user',
            'email': 'test@user.com',
            'password': 'test1234password'
        }
        response = self.client.post(CREATE_ADMIN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        admin = get_user_model().objects.get(**response.data)
        self.assertTrue(admin.check_password(payload['password']))
        self.assertNotIn('password', response.data)
    
    def test_admin_already_exist(self):
        """Testing Can not create an admin that exists."""
        payload = {
            'username': 'testuser',
            'name': 'test user',
            'email': 'test@user.com',
            'password': 'test1234password'
        }
        create_admin(**payload)
        response = self.client.post(CREATE_ADMIN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_short_password(self):
        """Testing that the admin should use a password with at least 6 characters"""
        payload = {
            'username': 'testuser',
            'name': 'test user',
            'email': 'test@user.com',
            'password': '12345'
        }
        response = self.client.post(CREATE_ADMIN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        admincreated = get_user_model().objects.filter(
            username=payload['username']
        ).exists()
        self.assertFalse(admincreated)
    
    def test_create_token_for_admin(self):
        """Test to get a token when the admin login"""
        payload = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'a1234test'
        }
        create_admin(**payload)
        response = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_for_invalid(self):
        """Test that the token is not created for invalid credentials (wrong password and username)"""
        create_admin(username='testusername', email='test@test.com', password='test124pas')
        payload = {
            'username': 'testusername',
            'email': 'test@test.com',
            'password': 'test1234pas'
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            'username': 'wrongtest',
            'password': 'doesnotmatter',
            'email': 'doesnt@matter.either'
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        