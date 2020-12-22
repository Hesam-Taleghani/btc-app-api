from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

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
    title = models.CharField(max_length=50, default="BTC Admin", blank=True, null=True)
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
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, blank=True, null=True)
    abreviation = models.CharField(max_length=5)
    is_covered = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.abreviation
