import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken



@pytest.fixture()
def api_client():
    client = APIClient()
    return client


@pytest.fixture()
def common_user():
    user = User.objects.create_user(
        username="test_user",
        email="test_user@test.com",
        password="A@123456",
        is_active=False
    )
    return user


@pytest.fixture()
def active_user():
    user = User.objects.create_user(
        username="test_user",
        email="test_user@test.com",
        password="A@123456",
    )
    return user
