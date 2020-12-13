from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTest(TestCase):
    """Testing Costum Django Admin"""

    def setUp(self):
        """Set up function running before test, to create a admin and login,
        create a user to see the list."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username='adminstrator',
            email='admin@test.com',
            password='testadmin1234'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            username='testt',
            email='test@test.com',
            password='herasd1234',
            name='test',
            phone='091223567890'
        )
    
    def test_admin_page_users(self):
        """Test to check the users listed on admin page"""
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.phone)
    
    def test_user_change_adminpage(self):
        """Test to check the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_user_creat_adminpage(self):
        """Test to check the add user page works."""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

