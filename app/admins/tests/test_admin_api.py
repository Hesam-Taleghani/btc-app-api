from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_ADMIN_URL = reverse('admins:create')
TOKEN_URL = reverse('admins:token')
MY_PROFILE_URL = reverse('admins:me')

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
    
    def test_authentication_needed_for_profile(self):
        """Test that authentication is needed to see and update profile"""
        response = self.client.get(MY_PROFILE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
class PrivateAdminProfileApi(TestCase):
    """Test the profile for authorized admin"""

    def setUp(self):
        self.admin = create_admin(
            username='testadmin',
            name='test admin',
            email='test@admin.com',
            password='admin1234admin',
            phone='12345678',
            postal_code='123321',
            birth_date='2000-01-01',
            address='world, world',
            title='tester'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
    
    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in admin"""
        response = self.client.get(MY_PROFILE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'username': self.admin.username,
            'name': self.admin.name,
            'email': self.admin.email,
            'address': self.admin.address,
            'phone': self.admin.phone,
            'postal_code': self.admin.postal_code,
            'birth_date': self.admin.birth_date,
            'title': self.admin.title,
            'is_staff': False,
        })

    def test_post_profile_not_allowed(self):
        """Test that post method is not allowed on this url"""
        response = self.client.post(MY_PROFILE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_updating_admin_profile(self):
        """Test updating admin profile for logged in admins"""
        payload = {
            'name':'new name test',
            'email':'changed@test.com',
            'password':'newadminpassword'
        }
        response = self.client.patch(MY_PROFILE_URL, payload)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.name, payload['name'])
        self.assertTrue(self.admin.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        