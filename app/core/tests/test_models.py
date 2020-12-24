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
    
    def test_VirtualService_creation(self):
        """To Test creating virtual services, with and without price and cost"""
        service = models.VirtualService.objects.create(
            name = 'test service',
            price = 67.99,
            cost = 54,
            created_by = sample_user(),
        )

        self.assertEqual(service.price, 67.99)
        self.assertEqual(service.cost, 54)
        self.assertEqual(str(service), 'test service')

    def test_goal_creation(self):
        """Test that the marketing goals are created successfully"""
        admin = sample_user()
        goal = models.MarketingGoal.objects.create(
            trading_name='test goal',
            legal_name='test name',
            trading_address='test address',
            postal_code='1234567',
            land_line='44332211',
            bussines_field='test field',
            created_by=admin
        )
        self.assertEqual(goal.trading_name, 'test goal')
        self.assertEqual(goal.created_by, admin)
        self.assertEqual(goal.get_status_display(), 'In Waiting Queue')
    
    def test_pos_create(self):
        """Test to create a compoany, model, and a pos related to them, 
           1. Test to create a company, 2. Test to create a model for company,
           3. Test to create a pos with large serial number to get validation error
           4. Test a validate data for pos"""
        admin = sample_user()
        company = models.POSCompany.objects.create(
            name = 'testCompany',
            serial_number_length = 8,
            created_by = admin
        )
        self.assertEqual(company.name, 'testCompany')
        self.assertEqual(company.serial_number_length, 8)
        model = models.POSModel.objects.create(
            name='testModel',
            company=company,
            hardware_cost=25,
            software_cost=25,
            price=79.99,
            created_by=admin
        )
        self.assertEqual(model.name, 'testModel')
        self.assertEqual(model.price, 79.99)
        self.assertEqual(str(model), 'testCompany testModel')
        # with self.assertRaises(ValueError):
        #     models.POS.objects.create(serial_number='1234567890',
        #                               pos_type="D",
        #                               model=model,
        #                               created_by=admin)
        pos = models.POS.objects.create(
                serial_number='12345678',
                type="D",
                model=model,
                created_by=admin  
        )
        self.assertEqual(str(pos), 'testCompany testModel 12345678')
        self.assertEqual(pos.get_type_display(), 'Desktop')
        self.assertEqual(pos.serial_number, '12345678')