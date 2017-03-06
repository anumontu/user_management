from django.contrib.auth import hashers
from models import CustomUser
from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'age')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = hashers.make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = hashers.make_password(validated_data['password'])
        return super(UserSerializer, self).update(instance, validated_data)


class AuthenticationSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = ('key', 'user')
