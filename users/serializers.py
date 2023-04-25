
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import authenticate
from users.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.name
        token['gender'] = user.gender
        token['age'] = user.age
        return token


class UserEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "name", "age", "gender", 'introduction')
        #fields = '__all__'


class UserDataSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('email', 'name', 'age', 'gender', 'password', 'introduction')


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            set_token = MyTokenObtainPairSerializer.get_token(user)
            token = {
                'refresh': str(set_token),
                'access': str(set_token.access_token)
            }
            return {'token': token}
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."})



