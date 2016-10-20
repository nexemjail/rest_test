from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.serializers import CharField, ValidationError


class UserCreateSerializer(serializers.ModelSerializer):
    password = CharField(required=True, label='Enter password')
    password2 = CharField(required=True, label='Confirm password')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'password2',
        )
        extra_kwargs = {'password':
                            {'write_only': True}}

    def validate_password2(self, value):
        data = self.get_initial()
        pass1 = data.get('password')
        pass2 = value
        if pass1 != pass2:
            raise ValidationError('Passwords must match!')
        return pass2

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    username = CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }