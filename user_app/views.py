from django.contrib.auth import hashers
from django.http import Http404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from models import CustomUser
from user_app.serializers import AuthenticationSerializer
from user_app.serializers import TokenSerializer
from user_app.serializers import UserSerializer
from user_app.serializers import UserUpdateSerializer
from . import exceptions
from .permissions import AuthorizationPermission


class UserProfile(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, AuthorizationPermission)

    def get_object(self, user_id):
        self.check_object_permissions(self.request, user_id)
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise Http404

    def get_user(self, request, user_id, format=None):
        user = self.get_object(user_id)
        user = UserSerializer(user)
        return Response(user.data)

    def update_user(self, request, user_id, format=None):
        user = self.get_object(user_id)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = hashers.make_password(serializer.validated_data['password'])

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def create_user(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = hashers.make_password(serializer.validated_data['password'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Authenticate(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def authenticate_user(self, request, format=None):
        serializer = AuthenticationSerializer(data=request.data)
        data = serializer.initial_data
        email = data.get('email')
        password = data.get('password')
        try:
            user = CustomUser.objects.get(email=email)
            authenticated = user.check_password(password)
            if not authenticated:
                raise exceptions.AuthenticationFailed('Bad Credentials')
        except CustomUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('Bad Credentials')
        token, created = Token.objects.get_or_create(user=user)
        serializer = TokenSerializer(token)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Logout(viewsets.ViewSet):
    def logout_user(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
