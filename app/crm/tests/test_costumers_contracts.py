from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Costumer, Contract, POSCompany, PosModel, POS, VirtualService, ContractService, ContractPOS, PaperRoll, Payment, MIDRevenue
from crm.serializers import CostumerMiniSerializer, ContractListSerializer, ContractDetailSerializer, ContractPosSerializer, ContractServiceSerializer, CostumerPaperrollSerializer


ALL_COSTUMER_URL = reverse('crm:all-costumers')
COSTUMER_URL = reverse('crm:costumer-list')
CONTRACT_URL = reverse('crm:contract-list')

def contract_pos_url(contract_id):
    return reverse('crm:contract-pos', args=[contract_id])

def contract_service_url(contract_id):
    return reverse('crm:contract-service', args=[contract_id])

def costumer_paperroll_url(costumer_id):
    return reverse('crm:contract-paperroll', args=[costumer_id])

def contract_payment_url(contract_id):
    return reverse('crm:contract-payment', args=[contract_id])

def contracr_mid_url(contract_id):
    return reverse('crm:contract-mid', args=[contract_id])

def contract_data_url(contract_id):
    return reverse('crm:contract-detail', args=[contract_id])

def create_service(name, admin):
    service = VirtualService.objects.create(
        name=name,
        price=12,
        cost=10,
        created_by=admin
    )
    return service

def create_pos(name, admin):
    """sample pos company, model and pos"""
    company = POSCompany.objects.create(
        name='Test Company',
        serial_number_length=5,
        created_by=admin
    )
    model = PosModel.objects.create(
        name=name,
        company=company,
        hardware_cost=12,
        software_cost=12,
        created_by=admin,
        price=50
    )
    pos = POS.objects.create(
        serial_number='12345',
        type='D',
        model=model,
        created_by=admin
    )
    return pos

def create_costumer(name, admin):
    """Sample costumer"""
    costumer = Costumer.objects.create(
            trading_name = name,
            legal_name = name,
            business_type = 'ET',
            legal_entity = 'ST',
            registered_address = name,
            registered_postal_code = '0123',
            business_postal_code = '0123',
            company_number = '0123',
            land_line = '0123',
            business_email = 'Test@Test.Test',
            director_name = name,
            director_phone = '0123',
            director_email = 'Test@Test.Test',
            director_address = name,
            director_postal_code = '0123',
            sort_code = '0123',
            issuing_bank = 'Test',
            account_number = '0123',
            business_bank_name = name,
            created_by = admin,
            last_updated_by = admin
        )
    return costumer

def create_contract(costumer, admin, date):
    """Sample Contract"""
    contract = Contract.objects.create(
        face_to_face_saled=10,
        atv=10.00,
        annual_card_turnover=10.00,
        annual_total_turnover=10.00,
        interchange=0.5,
        authorizathion_fee=0.5,
        pci_dss=0.5,
        acquire_name='EP',
        m_id='12345',
        start_date=date,
        end_date=date,
        created_by=admin,
        costumer=costumer
    )
    return contract


class CostumerTest(TestCase):
    """Test for the costumers and contracts and dependencies"""

    def setUp(self):
        self.client = APIClient()

    def login(self):
        """To login as an admin"""
        self.admin = get_user_model().objects.create_user(username='testuser',
                                                     email='test@admin.com',
                                                     password='testpassword')
        self.client.force_authenticate(self.admin)

    def test_login_required(self):
        """Test to login is required fo contracts and costumer pages"""
        response = self.client.get(COSTUMER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_costumer_mini_list(self):
        """Test to get all the costumer's Id, Trading name and Legal Name"""
        self.login()
        costumer1 = create_costumer('Test 1', self.admin)
        costumer2 = create_costumer('Test 2', self.admin)
        response = self.client.get(ALL_COSTUMER_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CostumerMiniSerializer(Costumer.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_contract_costumer(self):
        """Test to create a valid costumer, contract and dependencies via API"""
        self.login()
        payload_cos = {
            'trading_name': 'Test',
            'legal_name': 'Test',
            'business_type': 'ET',
            'legal_entity': 'ST',
            'registered_address': 'Test',
            'registered_postal_code': '0123',
            'business_postal_code': '0123',
            'company_number': '0123',
            'land_line': '0123',
            'business_email': 'Test@Test.Test',
            'director_name': 'Test',
            'director_phone': '0123',
            'director_email': 'Test@Test.Test',
            'director_address': 'Test',
            'director_postal_code': '0123',
            'sort_code': '0123',
            'issuing_bank': 'Test',
            'account_number': '0123',
            'business_bank_name': 'Test'
        }
        response = self.client.post(COSTUMER_URL, payload_cos)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Costumer.objects.filter(trading_name='Test').exists())
        id = response.data['id']
        payload_con = {
            'face_to_face_saled': 10,
            'atv': 10.00,
            'annual_card_turnover': 10.00,
            'annual_total_turnover': 10.00,
            'interchange': 0.5,
            'authorizathion_fee': 0.5,
            'pci_dss': 0.5,
            'acquire_name': 'EP',
            'm_id': '12345',
            'start_date': '2020-12-12',
            'end_date': '2020-12-12',
            'created_by': self.admin,
            'costumer': id
        }
        response = self.client.post(CONTRACT_URL, payload_con)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Contract.objects.filter(costumer=id).exists())

    def test_list_contracts(self):
        """Test to get contract list"""
        self.login()
        costumer = create_costumer('Test', self.admin)
        contract1 = create_contract(costumer, self.admin, '2020-10-10')
        contract2 = create_contract(costumer, self.admin, '2020-11-11')
        contract3 = create_contract(costumer, self.admin, '2020-12-12')
        serializer = ContractListSerializer(Contract.objects.all(), many=True)
        response = self.client.get(CONTRACT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_adding_and_retrieving_dependencies_of_contract(self):
        """Test to add services and poses to contracts, and add payrolls, payments and mid revenous to costumers,
           Then test to retrieve all of the informations about contracts."""
        self.login()
        costumer = create_costumer('Test', self.admin)
        contract = create_contract(costumer, self.admin, '2020-12-12')
        pos = create_pos('Test', self.admin)
        service = create_service('Test', self.admin)
        poscon = {
            'pos': pos.id,
            'price': 12,
            'hardware_cost': 25,
            'software_cost': 25
        }
        response = self.client.post(contract_pos_url(contract.id), poscon)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ContractPOS.objects.filter(contract=contract.id).exists())
        sercon = {
            'service': service.id,
            'price': 12,
            'cost': 10
        }
        response = self.client.post(contract_service_url(contract.id), sercon)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ContractService.objects.filter(contract=contract.id).exists())
        paperroll = {
            'amount':3,
            'cost': 1,
            'price': 1.49,
            'direct_debit_cost': 0.2,
            'ordered_date': '2020-12-12 12:30:00',
            'created_by': self.admin
        }
        response = self.client.post(costumer_paperroll_url(contract.id), paperroll)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PaperRoll.objects.filter(costumer=costumer.id).exists())
        payment = {
            'date': '2020-12-12 12:30:00',
            'direct_debit_cost': 12
        }
        response = self.client.post(contract_payment_url(contract.id), payment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Payment.objects.filter(contract=contract.id).exists())
        mid = {
            'income': 12,
            'profit': 5,
            'date': '2020-12-12 12:30:00'
        }
        response = self.client.post(contracr_mid_url(contract.id), mid)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(MIDRevenue.objects.filter(contract=contract.id).exists())

        response = self.client.get(contract_data_url(contract.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ContractDetailSerializer(contract)
        self.assertEqual(response.data, serializer.data)

        response = self.client.get(costumer_paperroll_url(contract.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CostumerPaperrollSerializer(PaperRoll.objects.filter(costumer=costumer.id), many=True)
        self.assertEqual(response.data, serializer.data)
