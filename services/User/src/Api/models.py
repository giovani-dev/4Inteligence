import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from typing import Any


# class UserManager(AbstractUser):
class UserManager(BaseUserManager):
    def create_user(self, email, password, is_admin=False, **extra_fields):
        # now = datetime.now()
        email = self.normalize_email(email)
        user = self.model(email=email, is_admin=is_admin, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password, **extra_fields):
        user = self.create_user(email, user_name, password, True, **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user


# Create your models here.
class Login(AbstractBaseUser):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=False, null=False, unique=True, max_length=255)
    is_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_trusty = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'password', 'email']

    class Meta:
        db_table = 'login'


class Profile(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    login = models.OneToOneField(Login, null=False, blank=False, related_name='profile_user', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=False, blank=True)
    birth_date = models.DateField(null=False, blank=False)
    cpf = models.CharField(max_length=20, null=False, blank=False)
    cep = models.CharField(max_length=20, null=False, blank=False)
    address = models.CharField(max_length=150, null=False, blank=True)
    house_number = models.CharField(max_length=150, null=False, blank=True)
    district = models.CharField(max_length=150, null=False, blank=True)
    city = models.CharField(max_length=150, null=False, blank=True)
    state = models.CharField(max_length=150, null=False, blank=True)

    class Meta:
        db_table = 'profile'

    @property
    def email(self):
        return self.login.email

    @property
    def user_name(self):
        return self.login.user_name