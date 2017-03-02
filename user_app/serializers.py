from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        read_only_fields = ('username', 'email')
        extra_kwargs = {'password': {'write_only': True}}


class AuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key', 'user')
