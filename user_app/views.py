from django.contrib.auth import hashers
from models import CustomUser
from django.http import Http404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user_app.serializers import AuthenticationSerializer
from user_app.serializers import TokenSerializer
from user_app.serializers import UserSerializer
from user_app.serializers import UserUpdateSerializer
from . import exceptions


class UserProfile(APIView):
    @staticmethod
    def get_object(user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise Http404

    @staticmethod
    def authorize(request, user_id):
        if str(request.user.id) != user_id:
            raise exceptions.AuthorizationFailed('Not Authorized')

    def get(self, request, user_id, format=None):
        self.authorize(request, user_id)
        user = self.get_object(user_id)
        user = UserSerializer(user)
        return Response(user.data)

    def put(self, request, user_id, format=None):
        self.authorize(request, user_id)
        user = self.get_object(user_id)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = hashers.make_password(serializer.validated_data['password'])

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = hashers.make_password(serializer.validated_data['password'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Authenticate(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
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


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
