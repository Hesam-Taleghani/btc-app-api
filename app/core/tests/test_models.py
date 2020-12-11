from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTest(TestCase):
    """ Test class for core app"""

    def test_creat_user(self):
        """testing to creat e user is successful using email, username and password."""
        email = "test@test.com"
        username = "test"
        password = "Test1234"
        user = get_user_model().objects.create_user(
            email = email,
            username = username,
            password = password
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
        