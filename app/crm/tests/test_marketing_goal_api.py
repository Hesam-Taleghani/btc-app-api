from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import MarketingGoal

from crm.serializers import GoalSerializer, GoalDetailSerializer

def goal_url(id):
    return reverse('crm:marketinggoal-detail', args=[id])

GOAL_URL = reverse('crm:marketinggoal-list')


class TestGoal(TestCase):
    """Marketing Goal Test"""

    def setUp(self):
        self.client = APIClient()
    
    def login(self):
        """To login as an admin"""
        self.admin = get_user_model().objects.create_user(username='testuser',
                                                     email='test@admin.com',
                                                     password='testpassword')
        self.client.force_authenticate(self.admin)
    
    def test_login_requiered(self):
        """To check if login is requiered"""
        response = self.client.get(GOAL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_creating_goal(self):
        """To Test creating a new marketing goal"""
        self.login()
        payload = {
            'trading_name': 'Test Goal',
            'bussines_field': 'Sports',
            'status': 'P',
        }
        response = self.client.post(GOAL_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(MarketingGoal.objects.filter(trading_name='Test Goal').exists())
        
    def test_goal_list(self):
        """Test to retrieve all marketing goals"""
        self.login()
        goal1 = MarketingGoal.objects.create(trading_name='Goal Test 1', bussines_field='Test', status='P', created_by=self.admin)
        goal2 = MarketingGoal.objects.create(trading_name='Goal Test 2', bussines_field='Test', status='P', created_by=self.admin)
        response = self.client.get(GOAL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        goals = MarketingGoal.objects.all().order_by('trading_name')
        serializer = GoalSerializer(goals, many=True)
        self.assertEqual(response.data, serializer.data)
    
    def test_goal_detail(self):
        """Test to retrieve a marketing goal's detail"""
        self.login()
        goal = MarketingGoal.objects.create(trading_name='Goal Test', bussines_field='Test', status='P', created_by=self.admin)
        response = self.client.get(goal_url(goal.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = GoalDetailSerializer(goal)
        self.assertEqual(response.data, serializer.data)

    def test_goal_update(self):
        """Test for editing a marketing goal"""
        self.login()
        goal = MarketingGoal.objects.create(trading_name='Goal Test', bussines_field='Test', status='P', created_by=self.admin)
        payload = {
            'trading_name': 'Edit Test', 
            'bussines_field': 'Test',
            'status': 'W'
        }
        response = self.client.put(goal_url(goal.id), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        goal.refresh_from_db()
        self.assertEqual(goal.trading_name, 'Edit Test')
        self.assertEqual(goal.status, 'W')
