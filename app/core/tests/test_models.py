from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(username='testuser', email='test@admin.com', password='testpassword'):
    """Creates a sample user"""
    return get_user_model().objects.create_user(username, email, password)

def sample_country(name='test', code='000', 
                   abreviation='TST', is_covered=True):
    user = sample_user()
    return models.Country.objects.create(created_by=user, name=name, code=code, 
                                         abreviation=abreviation, is_covered=is_covered)

class ModelTest(TestCase):
    """ Test class for core app"""

    def test_creat_user(self):
        """testing to creat e user is successful using email, username, country and password."""
        email = "test@test.com"
        username = "testusercreate"
        password = "Test1234"
        country = sample_country()
        user = get_user_model().objects.create_user(
            email = email,
            username = username,
            password = password,
            nationality = country
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
    
    def test_requiered_email_field(self):
        """Testing that users can not be created without email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, username="test", password="12345678")

    def test_requiered_username_field(self):
        """Testing that users can not be created without username"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="test@test.com", username=None, password="12345678")

    def test_creat_superuser(self):
        """Testing to create a new superuser using the commandline."""
        user = get_user_model().objects.create_superuser(
            "superusertst",
            "superuser@test.com",
            password = "passwordforsuperuser"
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        
    def test_country_creation(self):
        """Test that creating a new country works"""
        country = models.Country.objects.create(
            created_by = sample_user(),
            name='test',
            code='010',
            abreviation='TST',
            is_covered=True
        )

        self.assertEqual(country.name, 'test')
        self.assertEqual(str(country), 'TST')
