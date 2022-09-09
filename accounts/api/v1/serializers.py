from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from rest_framework.serializers import (Serializer, ModelSerializer, CharField, ValidationError,
                                        EmailField, BooleanField)
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class RegistrationSerializer(ModelSerializer):
    email = EmailField(max_length=100, required=True)
    password1 = CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password1']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise ValidationError({'details': 'passwords does not match!'})
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as errors:
            raise ValidationError({'password': list(errors.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password1', None)
        validated_data['is_active'] = False
        return User.objects.create_user(**validated_data)
