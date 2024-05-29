from rest_framework import generics, status, views
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
import jwt
import logging
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner, IsAdmin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from .tasks import send_birthday_emails

success_logger = logging.getLogger('success_logger')
error_logger = logging.getLogger('error_logger')


class UserRegister(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            password = serializer.validated_data.get('password')
            obj = serializer.save()
            success_logger.info(f'User created with email {obj.email}')
            token = RefreshToken.for_user(user=obj).access_token
            domain = get_current_site(request=request).domain
            relativeLink = reverse('activate-account', args=(str(token),))
            absurl = f'http://{domain}{relativeLink}'
            subject = "Account Activation Link"
            body = f"Hello {obj.email},\n\nYour account has been created successfully. Below are your login credentials:\n\nEmail: {obj.email}\nPassword: {password}\n\nPlease click on the link below to activate your account:\n{absurl}"
            print('Execution is working till here!')
            send_mail(subject=subject, message=body, from_email='kundan221195@gmail.com', recipient_list=[obj.email])

            # Trigger birthday email task using celery
            # result = send_birthday_emails.delay()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_logger.error(f'Error saving the user data {serializer.errors}')
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UserListAPI(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_queryset(), many=True)
            success_logger.info('Users Fetched Successfully')
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error('Error fetching users data')
            return Response(data={'detail': 'Error Fetching users'}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsAPI(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwner]

    def get(self, request, *args, **kawargs):
        try:
            obj = self.get_object()
            serializer = self.get_serializer(obj)
            success_logger.info("User details fetched successfully")
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except PermissionDenied as e:
            return Response(data={'detail': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated as e:
            return Response(data={'detail': 'Not Authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            error_logger.error('Error Fetching user details')
            return Response(data={'detail':'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
    
    def patch(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            serializer = self.get_serializer(data=request.data, instance=obj, partial=True)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            success_logger.info(f"User {obj.username} updated successfully")
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except PermissionDenied as e:
            return Response(data={'detail': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated as e:
            return Response(data={'detail': 'Not Authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            error_logger.error('Error Updating user details')
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            serializer = self.get_serializer(data=request.data, instance=obj)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            success_logger.info(f"User {obj.username} updated successfully")
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except PermissionDenied as e:
            return Response(data={'detail': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)
        except NotAuthenticated as e:
            return Response(data={'detail': 'Not Authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            error_logger.error('Error Updating user details')
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountVerify(views.APIView):

    def get(self, request, token=None):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms=['HS256'])
            user = User.objects.get(pk=payload.get('user_id'))
            user.is_active = True
            user.save()
            return Response(data={'detail': 'Account activated successfully'}, status=status.HTTP_200_OK)
        except jwt.DecodeError:
            return Response(data={'detail': 'Token in expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response(data={'detail': 'Link in expired'}, status=status.HTTP_400_BAD_REQUEST)


        
class UserLoginAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            email_or_mobile = request.data.get('email_or_mobile')
            password = request.data.get('password')

            if '@' in email_or_mobile:
                user = authenticate(email=email_or_mobile, password=password)
            else:
                print(email_or_mobile)
                user = authenticate(mobile=email_or_mobile, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                user_role = user.role
                return Response(data={'access_token': access_token, 'refresh_token': refresh_token,'role': user_role}, status=status.HTTP_200_OK)
            else:
                return Response(data={'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response(data={'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

