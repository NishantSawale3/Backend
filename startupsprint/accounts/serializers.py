from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import re


UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'mobile', 'gender', 'dob', 'permanent_address', 'current_address', 'photo', 'signature', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = UserModel.objects.create(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user
    
    def validate_email(self, value):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_mobile(self, value):
        if self.instance is None or self.instance.mobile != value:  
            if UserModel.objects.filter(mobile=value).exists():
                raise serializers.ValidationError("Mobile number already exists.")
        return value
    
    def validate_photo(self, value):
        max_photo_size = 5 * 1024 * 1024  # 5MB limit
        if value.size > max_photo_size:
            raise serializers.ValidationError("The photo size exceeds the maximum allowed size 5 MB.")
        return value
    
    def validate_signature(self, value):
        max_signature_size_bytes = 1 * 1024 * 1024 
        if value.size > max_signature_size_bytes:
            raise serializers.ValidationError("Signature size cannot exceed 1 MB.")
        return value
    
    def validate_role(self, value):
        ROLE_CHOICES = ['loan_representative','operational_head','loan_sanctioning_officer','admin','account_head']
        if value not in ROLE_CHOICES:
            raise serializers.ValidationError(f"Invalid role. Valid roles are: {', '.join(ROLE_CHOICES.values())}")
        
        return value

    def validate_dob(self, value):
        min_birth_date = timezone.now().date() - timedelta(days=365 * 100)  # 100 years ago
        max_birth_date = timezone.now().date() - timedelta(days=365 * 18)   # 18 years ago

        # Check if the date of birth is within the allowed range
        if value > max_birth_date:
            raise serializers.ValidationError("You must be at least 18 years old")
        elif value < min_birth_date:
            raise serializers.ValidationError("You cannot be older than 100 years")
        return value
    
    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only alphabetic characters")
        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Last name must contain only alphabetic characters")
        return value
    
    def validate_gender(self, value):
        GENDER_CHOICES = ['male', 'female', 'transgender']
        if value not in GENDER_CHOICES:
            raise serializers.ValidationError(f"Invalid gender. Valid options are: {', '.join(GENDER_CHOICES)}")
        return value
    
    def validate(self, data):
        if 'password' not in data:
            raise serializers.ValidationError("Password is required")
        return data

    

