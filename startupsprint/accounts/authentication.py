from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class MobileNumberBackend(ModelBackend):
    def authenticate(self, request, mobile=None, password=None, **kwargs):
        try:
            user = User.objects.get(mobile=mobile)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
