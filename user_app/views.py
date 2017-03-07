from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from models import CustomUser
from user_app.serializers import AuthenticationSerializer, TokenSerializer, UserSerializer
from . import exceptions
from .permissions import AuthorizationPermission


class UserList(ListAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserProfile(RetrieveAPIView, UpdateAPIView):
    permission_classes = (IsAuthenticated, AuthorizationPermission)

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


class CreateUser(CreateAPIView):
    permission_classes = (AllowAny,)

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


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
        return Response(serializer.data, status=status.HTTP_200_OK)


class Logout(viewsets.ViewSet):
    def logout_user(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
