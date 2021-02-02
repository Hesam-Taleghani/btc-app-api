from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.core.exceptions import ValidationError


def percent_validator(data):
    if data > 100 or data < 0:
        raise ValidationError('Invalid Shareholder')


class UserManager(BaseUserManager):
    """The Manager Class for the cusomized djangp users."""

    def create_user(self, username, email, password=None, **extra_fields):
        """Creat and Save a new user into database by all the given fields."""
        if not username:
            raise ValueError('User Must Have Username!')
        if not email:
            raise ValueError('User Must Have Email Address!')
        user = self.model(email=self.normalize_email(email), username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """creating and saving a new superuser"""
        user = self.create_user(username, email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """The Costume User Model Works with username, has extra fields."""
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    title = models.CharField(max_length=110, default="BTC Admin", blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True, default=None)
    phone = models.CharField(max_length=30, blank=True, null=True, default=None)
    postal_code = models.CharField(max_length=25, blank=True, null=True, default=None)
    birth_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, default=None)
    email = models.EmailField(max_length=254)
    nationality = models.ForeignKey('Country', 
                                    on_delete=models.SET_NULL, blank=True, null=True, default=None, 
                                    related_name='admin_nationalities')
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, related_name="admins")

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'


class Country(models.Model):
    """The Countries model for codes and coverage and abreviations"""
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    abreviation = models.CharField(max_length=5)
    is_covered = models.BooleanField(default=True)
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='countries')

    def __str__(self):
        return self.abreviation
    
    def save(self, *args, **kwargs):
        """To save the default abreviaiton as the first three letters in capital."""
        if self.abreviation:
            super().save(*args, **kwargs)
        else:
            self.abreviation = self.name[:3].upper()
            super().save(*args, **kwargs)


class VirtualService(models.Model):
    """The Model for virtual services, such as phone pay"""
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    availability = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   blank=True, null=True, related_name='services')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class MarketingGoal(models.Model):
    """The model for marketing goals to add to the costumers"""
    trading_name = models.CharField(max_length=110)
    legal_name = models.CharField(max_length=110, blank=True, null=True)
    bussines_field = models.CharField(max_length=110)
    land_line = models.CharField(max_length=30, blank=True, null=True)
    trading_address = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=25, blank=True, null=True)
    decision_maker = models.CharField(max_length=110, blank=True, null=True)
    mobile = models.CharField(max_length=27, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    status_choices = [
        ("A", "Accepted"),
        ("R", "Rejected"),
        ("W", "In Waiting Queue"),
        ("P", "Pending")
    ]
    status = models.CharField(max_length=20, choices=status_choices, default="W")
    note = models.TextField(blank=True, null=True, default=None)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name="goals",
                                   on_delete=models.SET_NULL, blank=True, null=True)
    last_update = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name="goals_updated",
                                    on_delete=models.SET_NULL, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.trading_name


class POSCompany(models.Model):
    """The model for POS companied"""
    name = models.CharField(max_length=110)
    serial_number_length = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   blank=True, null=True, related_name='pos_companies')
    
    def __str__(self):
        return self.name


class PosModel(models.Model):
    """Models of the POS making companies"""
    name = models.CharField(max_length=110)
    company = models.ForeignKey('POSCompany', on_delete=models.CASCADE, related_name='pos_models')
    hardware_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    software_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   blank=True, null=True, related_name='pos_models_created')
    
    def __str__(self):
        return str(self.company) + ' ' + self.name


class POS(models.Model):
    """Model for all the POSes"""
    serial_number = models.CharField(max_length=255)
    type_choices = [
        ("D", "Desktop"),
        ("M", "Mobile"),
        ("P", "Portable")
    ]
    type = models.CharField(max_length=25, choices=type_choices)
    model = models.ForeignKey('POSModel', on_delete=models.CASCADE, related_name='poses')

    note = models.TextField(blank=True, null=True, default=None)

    ownership = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    status = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   blank=True, null=True, related_name='poses_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.model) + ' ' + self.serial_number
    
    def clean(self, *args, **kwargs):
        if len(self.serial_number) != self.model.company.serial_number_length:
            raise ValidationError('Serial number length is not valid.')
        super(POS, self).clean(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(POS, self).save(*args, **kwargs)


class Costumer(models.Model):
    """The model for only costumers(mercheants)"""
    trading_name = models.CharField(max_length=110)
    legal_name = models.CharField(max_length=110)
    business_choices = [
        ("Acc", "Accommodation"), ("AcAu", "Accountants and Auditors"),
        ("BCM", "Builders, Carpenters and Materials"), ("CF", "Carpets nd Floornig"),
        ("Cat", "Caterers"), ("CNE", "Cinema, Nightclub and Entertainment"),
        ("CMS", "Cleaning and Maintenance Servises"), ("CA", "Clothing and Accessories"),
        ("ET", "Education and Trainig"), ("Est", "Estate Agents"),
        ("FDN", "Food, Drink and Newsagents"), ("Fur", "Furniture"),
        ("GCL", "Garden Centers and Landscaping"), ("GAC", "Gift Shopes, Arts and Crafts"),
        ("HB", "Hair and Beauty"), ("HMS", "Health and Mediacal Services"),
        ("HPA", "Heating, Plumping and Air Conditioning"), ("HAD", "Home Appliances and Decor"),
        ("Jew", "Jewellery"), ("Lth", "Leather Goods"),
        ("MSP", "Motor Sales, Servicing and parts"), ("Pet", "Pet Services"),
        ("PMS", "Petrol and Motorway Service Stations"), ("Pho", "Photography"),
        ("RPF", "Restaurants, Pubs and Fast Food"), ("SRF", "Sports and Recreation Faculties"),
        ("Txi", "Taxis"), ("TTA", "Theaters and Ticket Agencies"),
        ("Oth", "Other")
    ]
    business_type = models.CharField(max_length=50, choices=business_choices)
    legal_entity_choices = [
        ("ST", "Sole Trader"), ("Pa", "Partnership"),
        ("PrLC", "Private Limited Company"), ("PuLC", "Public Limited Company"),
        ("LLP", "Limited Liability Partnership"), ("Ch", "Charity"),
        ("Oth", "Other")
    ]
    legal_entity = models.CharField(max_length=50, choices=legal_entity_choices)
    business_date = models.DateField(blank=True, null=True)
    registered_address = models.CharField(max_length=510)
    registered_postal_code = models.CharField(max_length=50)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, 
                                   blank=True, null=True,
                                   related_name='costumer_location')
    business_postal_code = models.CharField(max_length=50)
    company_number = models.CharField(max_length=50)
    land_line = models.CharField(max_length=25)
    business_email = models.EmailField(max_length=255,)
    website = models.CharField(max_length=255, blank=True, null=True)

    director_name = models.CharField(max_length=110)
    director_phone = models.CharField(max_length=55)
    director_email = models.EmailField(max_length=255)
    director_address = models.CharField(max_length=255)
    director_postal_code = models.CharField(max_length=55)
    director_nationality = models.ForeignKey('Country', related_name='directors',
                                            on_delete=models.SET_NULL, blank=True, null=True)
    director_birth_date = models.DateField(blank=True, null=True)

    note = models.TextField(blank=True, null=True, default=None)

    sort_code = models.CharField(max_length=55)
    issuing_bank = models.CharField(max_length=110)
    account_number = models.CharField(max_length=110)
    business_bank_name = models.CharField(max_length=110)
    # pob = models.FileField(_(""), upload_to=None, max_length=100)
    # kyc1_id = models.FileField(_(""), upload_to=None, max_length=100)
    # kyc2_address_proof = models.FileField(_(""), upload_to=None, max_length=100)
    # kyb_peremises_photo = models.FileField(_(""), upload_to=None, max_length=100)
    # kyb_trading_address_proof = models.FileField(_(""), upload_to=None, max_length=100)
    # acquire_application = models.FileField(_(""), upload_to=None, max_length=100)
    # financial_report = models.FileField(_(""), upload_to=None, max_length=100)
    # vat_return = models.FileField(_(""), upload_to=None, max_length=100)
    # fd_consent = models.FileField(_(""), upload_to=None, max_length=100)
    # credit_search = models.FileField(_(""), upload_to=None, max_length=100)
    partner_name = models.CharField(max_length=110, blank=True, null=True)
    partner_address = models.CharField(max_length=255, blank=True, null=True)
    partner_nationality = models.ForeignKey('Country', related_name='partner_location',
                                            on_delete=models.SET_NULL, blank=True, null=True)
    shareholder = models.PositiveIntegerField(validators=[percent_validator,], blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   blank=True, null=True, related_name='costumers_created')
    updated_at = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   blank=True, null=True, related_name='costumers_last_updated')

    def __str__(self):
        return str(self.trading_name) + ' ' + self.legal_name
    
    def clean(self, *args, **kwargs):
        if self.business_bank_name != self.legal_name:
            raise ValidationError('Business Bank Name and Legal Name should be the same.')
        super(Costumer, self).clean(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        if self.legal_entity == "ST":
            self.partner_name = None
            self.partner_address = None
            self.partner_nationality = None
            self.shareholder = None
        super(Costumer, self).save(*args, **kwargs)


class TradingAddress(models.Model):
    """The model to save Trading addresses for costumers"""
    address = models.CharField(max_length=510)
    costumer = models.ForeignKey('Costumer', on_delete=models.CASCADE, related_name='trading_address')

    def __str__(self):
        return self.address


class Contract(models.Model):
    """The model to store the contracts"""
    costumer = models.ForeignKey('Costumer', on_delete=models.CASCADE, related_name='contracts')
    face_to_face_saled = models.PositiveIntegerField(validators=[percent_validator,])
    atv = models.DecimalField(max_digits=12, decimal_places=2)
    annual_card_turnover = models.DecimalField(max_digits=12, decimal_places=2)
    annual_total_turnover = models.DecimalField(max_digits=12, decimal_places=2)
    interchange = models.FloatField()
    authorizathion_fee = models.FloatField()
    pci_dss = models.FloatField()
    american_express_fee = models.FloatField(blank=True, null=True)
    acquire_name_choices = [
        ("EP", "Emerchant Pay"), ("FD", "First Data")
    ]
    acquire_name = models.CharField(max_length=25, choices=acquire_name_choices)
    m_id = models.CharField(max_length=55, blank=True, null=True)
    e_commerce_m_id = models.CharField(max_length=55, blank=True, null=True)
    amex_m_id = models.CharField(max_length=55, blank=True, null=True)
    t_id = models.CharField(max_length=55, blank=True, null=True)
    pci_due_date = models.DateField(blank=True, null=True)
    live_date = models.DateField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   blank=True, null=True, related_name='contracts_created')
    
    def __str__(self):
        return str(self.costumer) + ' ' + self.get_acquire_name_display()
    

class PaperRoll(models.Model):
    """The model foe every paper roll orders"""
    costumer = models.ForeignKey('Costumer', on_delete=models.CASCADE, related_name='paper_rolls')
    amount = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    direct_debit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    ordered_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   blank=True, null=True, related_name='paper_rolls_created')
    
    def __str__(self):
        return str(self.costumer) + ' ' + str(self.amount) + ' ' + str(self.ordered_date)


class Payment(models.Model):
    """The model for Direct Debit Pays of the contract"""
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, related_name='payments')
    date = models.DateTimeField()
    direct_debit_cost = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   blank=True, null=True, related_name='payments_created')


class MIDRevenue(models.Model):
    """The models to save all the contracts bonuses"""
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, related_name='mid_revenues')
    income = models.DecimalField(max_digits=12, decimal_places=2)
    profit = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   blank=True, null=True, related_name='mid_revenues_created')


class ContractPOS(models.Model):
    """The relation between contracts and POSes"""
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, related_name='contract_pos')
    pos = models.ForeignKey('POS', on_delete=models.CASCADE, related_name='pos_contract')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    cost = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   blank=True, null=True, related_name='contract_pos_created')
    

class ContractService(models.Model):
    """The relation between contracts and Virtual Services"""
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE, related_name='contract_service')
    service = models.ForeignKey('VirtualService', on_delete=models.CASCADE, related_name='service_contract')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    cost = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   blank=True, null=True, related_name='contract_service_created')
