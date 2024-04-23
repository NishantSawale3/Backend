from rest_framework import serializers
from .models import User
import datetime

class UserSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(format='%Y-%m-%d')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile', 'dob', 'email', 'gender', 'password', 'permanent_address', 'current_address', 'photo', 'signature', 'role', 'is_active']

    def create(self, value):
        if 'role' not in value:
            value['role'] = 'customer'
        return User.objects.create_user(**value)
    
    def validate_dob(self, value):
        today = datetime.datetime.now().date()
        if value > today:
            raise serializers.ValidationError('Date of birth cannot be allowed of future dates')
        return value
        
    def validate_first_name(self, value):
        min_length = 2
        max_length = 30
        if len(value) < min_length or len(value) > max_length:
            raise serializers.ValidationError(f'First name must be between {min_length} and {max_length} characters')
    
        if not value.isalpha():
            raise serializers.ValidationError(f'First name must contain only letters')
        
        return value
    
    def validate_last_name(self, value):
        min_length = 2
        max_length = 30
        if len(value) < min_length or len(value) > max_length:
            raise serializers.ValidationError(f'Last name must be between {min_length} and {max_length} characters')
        
        if not value.isalpha():
            raise serializers.ValidationError(f'Last name must contain only letters')
        
        return value
    
    def validate_photo(self, value):
        if value.content_type == ['image/jpeg', 'image/png', 'image/jpg']:
            raise serializers.ValidationError(f'only JPEG, JPG and PNG images are supported')
        
        max_size = 5 * 1024 * 1024      # 5MB
        if value.size > max_size:
            raise serializers.ValidationError(f'Image size must be less than {max_size} bytes')
    
        return value

    def validate_signature(self, value):
        if value.content_type == ['image/jpeg', 'image/png', 'image/jpg']:
            raise serializers.ValidationError(f'only JPEG, JPG and PNG images are supported')
        
        max_size = 2 * 1024 * 1024      # 2MB
        if value.size > max_size:
            raise serializers.ValidationError(f'Image size must be less than {max_size} bytes')
    
        return value
    
    def validate_mobile(self, value):
        max_length = 13
        if len(value) < max_length or len(value) > max_length:
            raise serializers.ValidationError('Invalid Number') 
        return value
    
    def validate_permanent_address(self, value):
        min_length = 20
        if len(value) < min_length:
            raise serializers.ValidationError('Permanent address must have atleast 20 characters')
        return value
    
    def validate_current_address(self, value):
        max_length = 20
        if len(value) < max_length:
            raise serializers.ValidationError('Invalid Current Address')
        return value
    
    def validate_password(self, value):
        min_length = 8
        if len(value) < min_length:
            raise serializers.ValidationError('Password must be contain at least 8 characters')
        return value

class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def create(self, value):
        new_password = value.get('new_password')
        confirm_password = value.get('confirm_password')
        if new_password != confirm_password:
            raise serializers.ValidationError('New password and confirm password must be the same')
        return value

    def validate_old_password(self, value):
        min_length = 8
        if len(value) < min_length:
            raise serializers.ValidationError('Password must be contain at least 8 characters')
        return value
    
    def validate_new_password(self, value):
        min_length = 8
        if len(value) < min_length:
            raise serializers.ValidationError('Password must be contain at least 8 characters')
        return value


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UpdatePasswordEmailSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def create(self, value):
        password = value.get('password')
        confirm_password = value.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('Password and confirm_password must be the same')
        return value

    def validate_password(self, value):
        min_length = 8
        if len(value) < min_length:
            raise serializers.ValidationError('Password must be contain at least 8 characters')
        return value