from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.core.exceptions import ValidationError

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

    def create_superuser(self, username, email, password):
        """creating and saving a new superuser"""
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """The Costume User Model Works with username, has extra fields."""
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    title = models.CharField(max_length=110, default="BTC Admin", blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    postal_code = models.CharField(max_length=25, blank=True, null=True)
    birth_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    email = models.EmailField(max_length=254)
    nationality = models.ForeignKey('Country', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'


class Country(models.Model):
    """The Countries model for codes and coverage and abreviations"""
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    abreviation = models.CharField(max_length=5)
    is_covered = models.BooleanField(default=True)
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   blank=True, null=True)
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
    note = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name="creator",
                                   on_delete=models.SET_NULL, blank=True, null=True)
    last_update = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name="Updated_admin",
                                    on_delete=models.SET_NULL, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.trading_name


class POSCompany(models.Model):
    """The model for POS companied"""
    name = models.CharField(max_length=110)
    serial_number_length = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   blank=True, null=True)
    
    def __str__(self):
        return self.name


class POSModel(models.Model):
    """Models of the POS making companies"""
    name = models.CharField(max_length=110)
    company = models.ForeignKey('POSCompany', on_delete=models.CASCADE)
    hardware_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    software_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   blank=True, null=True)
    
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
    model = models.ForeignKey('POSModel', on_delete=models.CASCADE)
    ownership = models.BooleanField(default=True)
    status = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.model) + ' ' + self.serial_number
