from rest_framework import generics
from .serializers import (
    RegistrationSerializer,
    ActivationResendSerializer,
    ChangePasswordSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ..utilities import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from mail_templated import EmailMessage
from django.conf import settings


User = get_user_model()


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = serializer.validated_data["username"]
            email = serializer.validated_data["email"]
            data = {
                "details": "User created successfully.",
                "username": username,
                "email": email,
            }
            user_obj = get_object_or_404(User, username=username)
            token = self.get_token_for_user(user_obj)
            email = EmailMessage(
                template_name="email/activation_email.tpl",
                context={"token": token},
                from_email="from@admin.com",
                to=[email],
            )
            EmailThread(email_obj=email).start()
            return Response(data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get_token_for_user(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationAPIView(APIView):
    """
    Activating new user account
    """

    @staticmethod
    def get(request, token, *args, **kwargs):
        try:
            token = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"details": "Token has been expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "Token is not valid."}, status=status.HTTP_400_BAD_REQUEST
            )
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_active:
            return Response({"details": "Your account has already been activated."})
        user_obj.is_active = True
        user_obj.save()
        return Response({"details": "Your account has been successfully activated."})


class ActivationResendAPIView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_token_for_user(user_obj)
        email = EmailMessage(
            template_name="email/activation_email.tpl",
            context={"token": token},
            from_email="from@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj=email).start()
        return Response(
            {"details": "Your activation code resend successfully."},
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def get_token_for_user(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ChangePasswordAPIView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": "Wrong password!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "Password changed successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthTokenAPIView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "username": user.username,
                "email": user.email,
            }
        )


class CustomDiscardAuthTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        request.user.auth_token.delete()
        return Response(
            {"details": "User logged out successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
