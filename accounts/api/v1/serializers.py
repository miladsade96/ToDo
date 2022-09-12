from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from rest_framework.serializers import (Serializer, ModelSerializer, CharField, ValidationError,
                                        EmailField, IntegerField)
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


class ActivationResendSerializer(Serializer):
    user_id = IntegerField(required=True)

    def validate(self, attrs):
        user_id = attrs.get("user_id")
        try:
            user_obj = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError({"details": "User does not exist!"})
        if user_obj.is_active:
            raise ValidationError({"details": "User is already activated!"})
        attrs["user"] = user_obj
        return super().validate(attrs)


class ChangePasswordSerializer(Serializer):
    def create(self, validated_data):
        return super(ChangePasswordSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(ChangePasswordSerializer, self).update(instance, validated_data)

    old_password = CharField(max_length=256, required=True)
    new_password = CharField(max_length=256, required=True)
    new_password1 = CharField(max_length=256, required=True)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise ValidationError({"details": "Password does not match!"})
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as errors:
            raise ValidationError({"new_password": list(errors.messages)})
        return super(ChangePasswordSerializer, self).validate(attrs)
