from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Country

from crm.serializers import CountrySerializer

COUNTRY_URL = reverse('crm:country-list')

class CountryApiTest(TestCase):
    """Test to retrieve the countries list"""

    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        """Test that log in is required for retieving countries list"""
        response = self.client.get(COUNTRY_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_country(self):
        """Test to create a country is successfull"""
        self.admin = get_user_model().objects.create_user(username='testuser',
                                                     email='test@admin.com',
                                                     password='testpassword')
        self.client.force_authenticate(self.admin)
        payload = {
            'name': 'test',
            'abreviation': 'TST',
            'code': '+1',
            'is_covered': True,
            'created_by': self.admin
        }
        response = self.client.post(COUNTRY_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Country.objects.filter(name='test').exists())
    
    def test_create_country_invalid(self):
        """Test Creation wont be completed with invalid payload
        1. unautherized, 2. invalid name"""
        payload = {
            'name': 'test',
            'abreviation': 'TST',
            'code': '+1',
            'is_covered': True,
        }
        response = self.client.post(COUNTRY_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.admin = get_user_model().objects.create_user(username='testuser',
                                                     email='test@admin.com',
                                                     password='testpassword')
        self.client.force_authenticate(self.admin)
        payload = {
            'name': '',
            'abreviation': 'TST',
            'code': '+1',
            'is_covered': True,
            'created_by': self.admin
        }
        response = self.client.post(COUNTRY_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retrieving_countries(self):
        """Test to get countries list after loging in"""
        self.admin = get_user_model().objects.create_user(username='testuser',
                                                     email='test@admin.com',
                                                     password='testpassword')
        self.client.force_authenticate(self.admin)
        Country.objects.create(name='Iran',
                               code='+98', 
                               abreviation='IRI', 
                               is_covered=False,
                               created_by=self.admin)
        Country.objects.create(name='United States Of America',
                               code='+1',
                               abreviation='USA',
                               is_covered=False,
                               created_by=self.admin)
        Country.objects.create(name='United Kingdom',
                               code='+44',
                               abreviation='UK',
                               is_covered=True,
                               created_by=self.admin)
        countries = Country.objects.all().order_by('abreviation')
        serializer = CountrySerializer(countries, many=True)
        response = self.client.get(COUNTRY_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    


