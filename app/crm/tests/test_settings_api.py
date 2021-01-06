from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Country, POSCompany

from crm.serializers import CountrySerializer, POSCompanySerializer

COUNTRY_URL = reverse('crm:country-list')
POS_COMPANY_URL = reverse('crm:poscompany-list')

class CountryApiTest(TestCase):
    """Test to retrieve the countries list"""

    def login(self):
        """To create and login as an admin"""
        self.admin = get_user_model().objects.create_user(username='testuser',
                                                     email='test@admin.com',
                                                     password='testpassword')
        self.client.force_authenticate(self.admin)

    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        """Test that log in is required for retieving countries list"""
        response = self.client.get(COUNTRY_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_country(self):
        """Test to create a country is successfull"""
        self.login()
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

        self.login()
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
        self.login()
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


class POSCompanyApiTest(TestCase):
    """The test case for pos company"""
    
    def login(self):   
        """To create and login as an admin"""
        self.admin = get_user_model().objects.create(
                                              username='testuser',
                                              email='test@user.com',
                                              password='testpass123',
                                              name='test user')
        self.client.force_authenticate(user=self.admin)
    
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test to check login is required for company url"""
        response = self.client.get(POS_COMPANY_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_valid_company(self):
        """Test to create a valid company via api"""
        self.login()
        company = {
            'name': 'test company',
            'serial_number_length': 10,
            'created_by': self.admin
        }
        response = self.client.post(POS_COMPANY_URL, company)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(POSCompany.objects.filter(name='test company').exists())

    def test_create_invalid_company(self):
        """Test that invalid data is not allowed"""
        self.login()
        company1 = {
            'name': '',
            'serial_number_length': 10,
            'created_by': self.admin
        }
        response = self.client.post(POS_COMPANY_URL, company1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        company2 = {
            'name': 'test company',
            'created_by': self.admin
        }
        response = self.client.post(POS_COMPANY_URL, company2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(POSCompany.objects.filter(serial_number_length=10).exists())
        self.assertFalse(POSCompany.objects.filter(name='test company').exists())

    def test_retrieving_pos_companies(self):
        """Test to get all companies that are created"""
        self.login()
        company1 = POSCompany.objects.create(
            name='company 1',
            serial_number_length=10,
            created_by=self.admin
        )
        company2 = POSCompany.objects.create(
            name='company 2',
            serial_number_length=12,
            created_by=self.admin
        )
        response = self.client.get(POS_COMPANY_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        companies = POSCompany.objects.all().order_by('name')
        serializer = POSCompanySerializer(companies, many=True)
        self.assertEqual(response.data, serializer.data)
