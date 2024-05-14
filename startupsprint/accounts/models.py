from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
#from .models import CustomUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, mobile, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name, last_name, mobile, password, **extra_fields)

class User(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'male'),
        ('female', 'female'),
        ('transgender', 'transgender')
    ]
    ROLE_CHOICES = [
        ('customer', 'customer'),
        ('loan_representative', 'loan representative'),
        ('operational_head', 'operational_head'),
        ('loan sanctioning officer', 'loan_sanctioning_officer'), 
        ('admin', 'admin'),
        ('account_head', 'account_head'),
    ]
    username = None
    dob = models.DateField(blank=True, default="2000-12-12")
    gender = models.CharField(max_length=11, choices = GENDER_CHOICES)
    email = models.EmailField(db_index=True, max_length=50, unique =True)
    permanent_address = models.TextField(blank=True, null=True)
    current_address = models.TextField(blank =True, null=True) 
    mobile = PhoneNumberField(region='IN', blank =True, null=True)
    photo = models.ImageField(blank=True, upload_to='photo/', null=True)
    signature = models.ImageField(blank=True, upload_to='signature/', null=True)
    role = models.CharField(max_length=24, choices = ROLE_CHOICES, blank =True, null=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'mobile')

    objects = CustomUserManager()

    class Meta:
        verbose_name ='User'
        verbose_name_plural ='Users'
