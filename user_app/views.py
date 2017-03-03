from django.contrib.auth import hashers
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['password'] = hashers.make_password(serializer.validated_data['password'])
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CreateUser(CreateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['password'] = hashers.make_password(serializer.validated_data['password'])
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
