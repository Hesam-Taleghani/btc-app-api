from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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
    name = models.CharField(max_length=60)
    # profile_picture = models.ImageField(upload_to=None)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    # nationality = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=25)
    birth_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'