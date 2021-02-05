from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Country, POSCompany, PosModel, POS, VirtualService, Costumer, Contract, ContractPOS, ContractService

from crm.serializers import CountrySerializer, POSCompanySerializer, PosModelSerializer, PosSerializer, ServiceSerializer

COUNTRY_URL = reverse('crm:country-list')
POS_COMPANY_URL = reverse('crm:poscompany-list')
POS_MODEL_URL = reverse('crm:posmodels-list')
POS_URL = reverse('crm:pos-list')
SERVICE_URL = reverse('crm:virtualservice-list')


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
            'is_covered': True
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
            'is_covered': True
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
            'serial_number_length': 10
        }
        response = self.client.post(POS_COMPANY_URL, company)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(POSCompany.objects.filter(name='test company').exists())

    def test_create_invalid_company(self):
        """Test that invalid data is not allowed"""
        self.login()
        company1 = {
            'name': '',
            'serial_number_length': 10
        }
        response = self.client.post(POS_COMPANY_URL, company1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        company2 = {
            'name': 'test company'
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


class PosModelTest(TestCase):
    """The Test case for pos company models"""

    def setUp(self):
        self.client = APIClient()

    def login(self):   
        """To create and login as an admin"""
        self.admin = get_user_model().objects.create(
                                              username='testuser',
                                              email='test@user.com',
                                              password='testpass123',
                                              name='test user')
        self.client.force_authenticate(user=self.admin)

    def test_login_required(self):
        """Test for login requirement on this page"""
        response = self.client.get(POS_MODEL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_posmodel(self):
        """Test to create a posmodel via valid data"""
        self.login()
        company = POSCompany.objects.create(
            name='company1',
            serial_number_length=12,
            created_by=self.admin
        )
        posmodel = {
            'name': 'name for pos model',
            'hardware_cost': 12,
            'software_cost': 5,
            'price': 23
        }
        response = self.client.post(reverse('crm:create-pos-model', args=[company.id]), posmodel)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PosModel.objects.filter(name='name for pos model').exists())
        self.assertEqual(PosModel.objects.get(name='name for pos model').company, company)

    def test_create_invalid_pos_model(self):
        """To Test that a model can not be created without a name"""
        self.login()
        company = POSCompany.objects.create(
            name='company',
            serial_number_length=10,
            created_by=self.admin
        )
        model = {
            'hardware_cost': 29.98,
            'software_cost': 12.55,
            'price': 49.99
        }
        response = self.client.post(reverse('crm:create-pos-model', args=[company.id]), model)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(PosModel.objects.filter(company=company).exists())

    def test_posmodel_list(self):
        """Test to retrieve all pos models"""
        self.login()
        company = POSCompany.objects.create(
            name='company',
            serial_number_length=10,
            created_by=self.admin
        )
        model1 = PosModel.objects.create(
            name='model 1',
            company=company,
            hardware_cost=12.62,
            software_cost=8.32,
            price=32.99,
            created_by=self.admin
        )
        model2 = PosModel.objects.create(
            name='model 2',
            company=company,
            hardware_cost=22.62,
            software_cost=18.32,
            price=59.99,
            created_by=self.admin
        )
        response = self.client.get(POS_MODEL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        models = PosModel.objects.all().order_by('name')
        serializer = PosModelSerializer(models, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_getting_models_company(self):
        """Test to get models of a company"""
        self.login()
        company1 = POSCompany.objects.create(
            name='company1',
            serial_number_length=10,
            created_by=self.admin
        )
        company2 = POSCompany.objects.create(
            name='company2',
            serial_number_length=10,
            created_by=self.admin
        )
        model1 = PosModel.objects.create(
            name='model 1',
            company=company1,
            hardware_cost=12.62,
            software_cost=8.32,
            price=32.99,
            created_by=self.admin
        )
        model2 = PosModel.objects.create(
            name='model 2',
            company=company1,
            hardware_cost=22.62,
            software_cost=18.32,
            price=59.99,
            created_by=self.admin
        )
        model3 = PosModel.objects.create(
            name='model 3',
            company=company2,
            hardware_cost=12.62,
            software_cost=8.32,
            price=32.99,
            created_by=self.admin
        )
        response = self.client.get(reverse('crm:company-models', args=[company1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        models = PosModel.objects.filter(company=company1)
        serializer = PosModelSerializer(models, many=True)
        self.assertEqual(response.data, serializer.data)


class PosTestCase(TestCase):
    """All the tests for poses"""

    def setUp(self):
        self.client = APIClient()

    def login(self):   
        """To create and login as an admin"""
        self.admin = get_user_model().objects.create(
                                              username='testuser',
                                              email='test@user.com',
                                              password='testpass123',
                                              name='test user')
        self.client.force_authenticate(user=self.admin)

    def test_login_required(self):
        """Test that login is required for pos url"""
        response = self.client.get(POS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_invalid_pos(self):
        """Test that a pos can not be created without serial number, type, model and invalid serial number length."""
        self.login()
        company = POSCompany.objects.create(
            name='company',
            serial_number_length=5,
            created_by=self.admin
        )
        posmodel = PosModel.objects.create(
            name='model',
            company=company,
            hardware_cost=12.62,
            software_cost=8.32,
            price=32.99,
            created_by=self.admin
        )
        pos1 = {
            'type':'D',
            'model':posmodel.id,
        }
        pos2 = {
            'serial_number':'48271',
            'model':posmodel.id,
        }
        pos3 = {
            'serial_number':'234',
            'type':'D',
            'model':posmodel.id,
        }
        response = self.client.post(POS_URL, pos1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(POS_URL, pos2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(POS_URL, pos3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(POS.objects.filter(model=posmodel).exists())

    def test_create_valid_pos(self):
        """Test to create a valid pos"""
        self.login()
        company = POSCompany.objects.create(
            name='company',
            serial_number_length=5,
            created_by=self.admin
        )
        posmodel = PosModel.objects.create(
            name='model',
            company=company,
            hardware_cost=12.62,
            software_cost=8.32,
            price=32.99,
            created_by=self.admin
        )
        pos = {
            'serial_number': '23004',
            'type': 'D',
            'model': posmodel.id,
        }
        response = self.client.post(POS_URL, pos)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(POS.objects.filter(serial_number='23004').exists())

    def test_pos_list(self):
        """Test to get all poses"""
        self.login()
        company = POSCompany.objects.create(
            name='company',
            serial_number_length=5,
            created_by=self.admin
        )
        posmodel = PosModel.objects.create(
            name='model',
            company=company,
            hardware_cost=12.62,
            software_cost=8.32,
            price=32.99,
            created_by=self.admin
        )
        pos1 = POS.objects.create(
            serial_number='20211',
            type='D',
            model=posmodel,
            created_by=self.admin
        )
        pos2 = POS.objects.create(
            serial_number='20203',
            type='D',
            model=posmodel,
            created_by=self.admin
        )
        poses = POS.objects.all().order_by('serial_number')
        serializer = PosSerializer(poses, many=True)
        response = self.client.get(POS_URL)
        self.assertEqual(response.data, serializer.data)

    def test_invalid_update(self):
        """Test that the serial number length should be valid to update the instance"""
        self.login()
        company = POSCompany.objects.create(
            name='company',
            serial_number_length=5,
            created_by=self.admin
        )
        posmodel = PosModel.objects.create(
            name='model',
            company=company,
            hardware_cost=12.62,
            software_cost=8.32,
            price=32.99,
            created_by=self.admin
        )
        pos = POS.objects.create(
            serial_number='20203',
            type='D',
            model=posmodel,
            created_by=self.admin
        )
        response = self.client.patch(reverse('crm:pos-detail', args=[pos.id]), {'serial_number': '2021'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        pos.refresh_from_db()
        self.assertEqual(pos.serial_number, '20203')

    def test_pos_update(self):
        """Test to edit a pos"""
        self.login()
        company = POSCompany.objects.create(
            name='company',
            serial_number_length=5,
            created_by=self.admin
        )
        posmodel = PosModel.objects.create(
            name='model',
            company=company,
            hardware_cost=12.62,
            software_cost=8.32,
            price=32.99,
            created_by=self.admin
        )
        pos = POS.objects.create(
            serial_number='20203',
            type='D',
            model=posmodel,
            created_by=self.admin
        )
        response = self.client.patch(reverse('crm:pos-detail', args=[pos.id]), {'serial_number': '20201'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pos.refresh_from_db()
        self.assertEqual(pos.serial_number, '20201')

    def test_pos_active(self):
        """To test activate and deactivating a pos"""
        self.login()
        company = POSCompany.objects.create(
            name='company',
            serial_number_length=5,
            created_by=self.admin
        )
        posmodel = PosModel.objects.create(
            name='model',
            company=company,
            hardware_cost=12.62,
            software_cost=8.32,
            price=32.99,
            created_by=self.admin
        )
        pos = POS.objects.create(
            serial_number='20203',
            type='D',
            model=posmodel,
            created_by=self.admin
        )
        response = self.client.post(reverse('crm:pos-active', args=[pos.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pos.refresh_from_db()
        self.assertFalse(pos.is_active)
        response = self.client.post(reverse('crm:pos-active', args=[pos.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pos.refresh_from_db()
        self.assertTrue(pos.is_active)


class ServiceTest(TestCase):
    """Test case for virtual services"""

    def setUp(self):
        self.client = APIClient()

    def login(self):   
        """To create and login as an admin"""
        self.admin = get_user_model().objects.create(
                                              username='testuser',
                                              email='test@user.com',
                                              password='testpass123',
                                              name='test user')
        self.client.force_authenticate(user=self.admin)

    def test_login_required(self):
        """Test that login is required"""
        response = self.client.get(SERVICE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_invalid_service(self):
        """Test to create with a duplicate name"""
        self.login()
        service1 = VirtualService.objects.create(
            name='Test Service',
            price=12.99,
            cost= 9.99
        )
        service2 = {
            'name': 'Test Service',
            'price': 15.99,
            'cost': 9.99
        }
        response = self.client.post(SERVICE_URL, service2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_valid_service(self):
        """Test to create a valid service"""
        self.login()
        service = {
            'name': 'Test Service',
            'price': 12.99,
            'cost': 9.99
        }
        response = self.client.post(SERVICE_URL, service)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(VirtualService.objects.filter(name='Test Service').exists())

    def test_retrieving_services(self):
        """Test to get all the services"""
        self.login()
        service1 = VirtualService.objects.create(
            name='Test Service1',
            price=15.99,
            cost=12.99
        )
        service2 = VirtualService.objects.create(
            name='Test Service2',
            price=22.99,
            cost=18.99
        )
        response = self.client.get(SERVICE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        services = VirtualService.objects.all()
        serializer = ServiceSerializer(services, many=True)
        self.assertEqual(serializer.data, response.data)

    def test_edit_service(self):
        """Test to edit a service"""
        self.login()
        service = VirtualService.objects.create(
            name='Test Service',
            price=15.99,
            cost=2.99
        )
        update = {
            'cost': 12
        }
        response = self.client.patch(reverse('crm:virtualservice-detail', args=[service.id]), update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        service.refresh_from_db()
        self.assertEqual(service.cost, 12)


class IsUsed(TestCase):
    """The class to check the is_used functionality"""

    def setUp(self):
        self.client = APIClient()

    def login(self):   
        """To create and login as an admin"""
        self.admin = get_user_model().objects.create(
                                              username='testuser',
                                              email='test@user.com',
                                              password='testpass123',
                                              name='test user')
        self.client.force_authenticate(user=self.admin)

    def test_country_used(self):
        """To Test that is a country used and get the correct response"""
        self.login()
        country = Country.objects.create(name='Iran',
                               code='+98', 
                               abreviation='IRI', 
                               is_covered=False,
                               created_by=self.admin)
        costumer = Costumer.objects.create(
                trading_name="test costumer",
                legal_name="test costumer",
                business_type="Pet",
                legal_entity="PuLC",
                business_date="2020-12-12",
                registered_address="test address",
                registered_postal_code="12345678",
                country=country,
                business_postal_code="4321",
                company_number="02112345678",
                land_line="09123456789",
                business_email="test@email.com",
                director_name="test director",
                director_phone="09312345678",
                director_email="director@test.email",
                director_address="where director lives",
                director_postal_code="000000",
                director_nationality=country,
                sort_code="1221",
                issuing_bank="test bank",
                account_number="0000-0000-0000-0000",
                business_bank_name="test costumer",
                partner_name="partner",
                partner_address="where partner lives",
                partner_nationality=country,
                created_by=self.admin,
                last_updated_by=self.admin)
        response = self.client.get(reverse('crm:country-used', args=[country.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['used'])
        country1 = Country.objects.create(name='United Kingdom',
                               code='+44', 
                               abreviation='UK', 
                               is_covered=True,
                               created_by=self.admin)
        response = self.client.get(reverse('crm:country-used', args=[country1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['used'])

    def test_company_used(self):
        """Test that company is used"""
        self.login()
        company = POSCompany.objects.create(name = 'Company',
                                            serial_number_length = 12,
                                            created_by=self.admin)
        model = PosModel.objects.create(name = 'Model',
                                        company = company,
                                        hardware_cost = 20,
                                        software_cost = 10,
                                        price = 40,
                                        created_by=self.admin)
        response = self.client.get(reverse('crm:company-used', args=[company.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['used'])
        company1 = POSCompany.objects.create(name = 'Company 1',
                                            serial_number_length = 12,
                                            created_by=self.admin)
        response = self.client.get(reverse('crm:company-used', args=[company1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['used'])

    def test_model_used(self):
        """Test that model is used"""
        self.login()
        company = POSCompany.objects.create(name = 'Company',
                                            serial_number_length = 12,
                                            created_by=self.admin)
        model = PosModel.objects.create(name = 'Model',
                                        company = company,
                                        hardware_cost = 20,
                                        software_cost = 10,
                                        price = 40,
                                        created_by=self.admin)
        pos = POS.objects.create(serial_number='012345678910',
                                 type='D',
                                 model=model,
                                 created_by=self.admin)
        model1 = PosModel.objects.create(name = 'Model 1',
                                        company = company,
                                        hardware_cost = 20,
                                        software_cost = 10,
                                        price = 40,
                                        created_by=self.admin)
        response = self.client.get(reverse('crm:model-used', args=[model.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['used'])
        response = self.client.get(reverse('crm:model-used', args=[model1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['used'])

    def test_pos_used(self):
        """Test that pos is used""" 
        self.login()
        country = Country.objects.create(name='Iran',
                               code='+98', 
                               abreviation='IRI', 
                               is_covered=False,
                               created_by=self.admin)
        company = POSCompany.objects.create(name = 'Company',
                                            serial_number_length = 12,
                                            created_by=self.admin)
        model = PosModel.objects.create(name = 'Model',
                                        company = company,
                                        hardware_cost = 20,
                                        software_cost = 10,
                                        price = 40,
                                        created_by=self.admin)
        pos = POS.objects.create(serial_number='012345678910',
                                 type='D',
                                 model=model,
                                 created_by=self.admin)
        pos1 = POS.objects.create(serial_number='012345238910',
                                 type='D',
                                 model=model,
                                 created_by=self.admin)
        costumer = Costumer.objects.create(
            trading_name="test costumer",
            legal_name="test costumer",
            business_type="Pet",
            legal_entity="PuLC",
            business_date="2020-12-12",
            registered_address="test address",
            registered_postal_code="12345678",
            country=country,
            business_postal_code="4321",
            company_number="02112345678",
            land_line="09123456789",
            business_email="test@email.com",
            director_name="test director",
            director_phone="09312345678",
            director_email="director@test.email",
            director_address="where director lives",
            director_postal_code="000000",
            director_nationality=country,
            sort_code="1221",
            issuing_bank="test bank",
            account_number="0000-0000-0000-0000",
            business_bank_name="test costumer",
            partner_name="partner",
            partner_address="where partner lives",
            partner_nationality=country,
            created_by=self.admin,
            last_updated_by=self.admin
        )
        contract = Contract.objects.create(
            costumer=costumer,
            face_to_face_saled=75,
            atv=23.12,
            annual_card_turnover=123.21,
            annual_total_turnover=1234.56,
            interchange=0.5,
            authorizathion_fee=0.5,
            pci_dss=0.5,
            acquire_name="EP",
            start_date="2020-12-12",
            end_date="2021-12-12",
            total_cost=210.00,
            total_price=270.00,
            created_by=self.admin
        )
        contract_pos = ContractPOS.objects.create(
            contract=contract,
            pos=pos,
            price=120.00,
            hardware_cost=100.00,
            software_cost=10.00,
            created_by=self.admin
        )
        response = self.client.get(reverse('crm:pos-used', args=[pos.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['used'])
        response1 = self.client.get(reverse('crm:pos-used', args=[pos1.id]))
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertFalse(response1.data['used'])

    def test_service_used(self):
        """Test that Service is used""" 
        self.login()
        country = Country.objects.create(name='Iran',
                               code='+98', 
                               abreviation='IRI', 
                               is_covered=False,
                               created_by=self.admin)
        costumer = Costumer.objects.create(
            trading_name="test costumer",
            legal_name="test costumer",
            business_type="Pet",
            legal_entity="PuLC",
            business_date="2020-12-12",
            registered_address="test address",
            registered_postal_code="12345678",
            country=country,
            business_postal_code="4321",
            company_number="02112345678",
            land_line="09123456789",
            business_email="test@email.com",
            director_name="test director",
            director_phone="09312345678",
            director_email="director@test.email",
            director_address="where director lives",
            director_postal_code="000000",
            director_nationality=country,
            sort_code="1221",
            issuing_bank="test bank",
            account_number="0000-0000-0000-0000",
            business_bank_name="test costumer",
            partner_name="partner",
            partner_address="where partner lives",
            partner_nationality=country,
            created_by=self.admin,
            last_updated_by=self.admin
        )
        contract = Contract.objects.create(
            costumer=costumer,
            face_to_face_saled=75,
            atv=23.12,
            annual_card_turnover=123.21,
            annual_total_turnover=1234.56,
            interchange=0.5,
            authorizathion_fee=0.5,
            pci_dss=0.5,
            acquire_name="EP",
            start_date="2020-12-12",
            end_date="2021-12-12",
            total_cost=210.00,
            total_price=270.00,
            created_by=self.admin
        )
        service = VirtualService.objects.create(name = 'service',
                                                price = 12,
                                                cost = 10,
                                                created_by= self.admin)
        contract_service = ContractService.objects.create(contract=contract,
                                                          service = service,
                                                          price=12,
                                                          cost=10,
                                                          created_by=self.admin)
        service1 = VirtualService.objects.create(name = 'service 1',
                                                price = 15,
                                                cost = 12,
                                                created_by= self.admin)
        response = self.client.get(reverse('crm:service-used', args=[service.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['used'])
        response = self.client.get(reverse('crm:service-used', args=[service1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['used'])
