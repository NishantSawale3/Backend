from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
#from .models import CustomUserManager



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
    REQUIRED_FIELDS = ('first name', 'last name', 'mobile')

    #objects = CustomUserManager()

    class Meta:
        verbose_name ='User'
        verbose_name_plural ='Users'
