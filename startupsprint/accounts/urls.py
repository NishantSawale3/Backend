from django.urls import path, include
from .views import *

urlpatterns = [
    path('user/', UserAPI.as_view(), name='user'),
    path('verify/', Verify_Email.as_view(), name='verify-email'),
    path('change_password/', ChangePasswordAPI.as_view(), name='change_password'),
    path('reset_password/', ResetUserPasswordAPI.as_view(), name='reset-password'),
    path('update_password/', UpdateUserPassword.as_view(), name='update-password')
]