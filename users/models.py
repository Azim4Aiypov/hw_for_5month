from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from utils.confirmation import set_confirmation_code  

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, phone_number=None, first_name=None, last_name=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)

        # Только суперпользователь требует обязательные поля
        if extra_fields.get('is_superuser', False):
            if not phone_number:
                raise ValueError('Superuser must have phone number')
            if not first_name:
                raise ValueError('Superuser must have first name')
            if not last_name:
                raise ValueError('Superuser must have last name')

        user = self.model(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, phone_number=None, first_name=None, last_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not phone_number:
            phone_number = '0000000000'
        if not first_name:
            first_name = 'Admin'
        if not last_name:
            last_name = 'User'

        return self.create_user(
            email, password=password,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthdate = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def generate_confirmation_code(self):
        self.is_active = False
        self.save()
        return set_confirmation_code(self.id)  
