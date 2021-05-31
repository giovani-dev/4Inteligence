# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from typing import Any
import uuid


class Login(AbstractBaseUser):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=False, null=False, unique=True, max_length=255)
    is_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_trusty = models.BooleanField(default=True)

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'password']


    def is_valid_field(self, field: str, value: Any) -> bool:
        for class_field in self.__dict__:
            if class_field == field and self.__dict__[class_field] == value:
                return True
        return False

    class Meta:
        managed = False
        db_table = 'login'