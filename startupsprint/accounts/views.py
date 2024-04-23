from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserSerializer, ChangePasswordSerializer, ResetPasswordEmailSerializer, UpdatePasswordEmailSerializer
from .models import User

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import update_session_auth_hash

from rest_framework_simplejwt.tokens import RefreshToken
import jwt
import logging
import datetime

loggers = logging.getLogger('loggers')

class UserAPI(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            obj.is_active = False
            obj.save()
            current_site = get_current_site(request).domain
            relative_link = reverse('verify-email')

            subject = 'Verfiy Email'
            email = request.data.get('email')

            token = RefreshToken.for_user(obj).access_token
            # first_name = request.data.get('first_name')

            absolute_url = f'http://{current_site}{relative_link}?token={token}'

            message = f'Hey !!! \n Click This link to verify your email \n {absolute_url}'
            send_mail(
                subject = subject,
                recipient_list = [email],
                message = message,
                from_email = settings.EMAIL_HOST_USER,  
            )
            loggers.info(f'Email has been sent to {email} at: {datetime.datetime.now()}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # loggers.error(f'User {email} made mistakes at: {datetime.datetime.now()}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Verify_Email(APIView):

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            customer = User.objects.get(id=payload['user_id'])
            print(customer)
            customer.is_active = True
            customer.save()
            loggers.info(f'customer id: {customer} has been verified at: {datetime.datetime.now()}')
            return Response(data={'email': 'Successfully activated'}, status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as identifire:
            return Response(data={'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifire:
            return Response(data={'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                print("Password matched")
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ResetUserPasswordAPI(APIView):

    def post(self, request):
        serializer = ResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
            except User.DoesNotExist:
                return Response(data={'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            # current_site = get_current_site(request).domain
            # relative_link = reverse('update-password')

            email = serializer.validated_data['email']

            token = RefreshToken.for_user(user).access_token

            absolute_url = f'http://localhost:3000/accounts/update_password/{token}'

            message = f'Click This url ro change your password \n {absolute_url}'

            send_mail(
                subject='Reset Password Mail',
                recipient_list=[email],
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                fail_silently=False
            )
            return Response({'message': 'Email link has been sent to your email to rest your password'}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateUserPassword(APIView):

    def post(self, request):
        serializer = UpdatePasswordEmailSerializer(data=request.data)
        token = request.data.get('token')
        # print('TOKEN---->', token)
        if serializer.is_valid():
            new_password = serializer.validated_data['password']
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                # print('PAYLOAD----->', payload)
                user = User.objects.get(id=payload['user_id'])

                user.set_password(new_password)
                user.save()
                send_mail(
                    subject='Password Changed',
                    recipient_list=[user.email],
                    message='Your password has been changed successfully',
                    from_email=settings.EMAIL_HOST_USER,
                    fail_silently=False
                )
                return Response(data={'Password': 'Password changed Successfully'}, status=status.HTTP_201_CREATED)
            except jwt.ExpiredSignatureError as identifire:
                return Response(data={'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.exceptions.DecodeError as identifire:
                return Response(data={'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

