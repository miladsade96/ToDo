import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.fixture()
def api_client():
    client = APIClient()
    return client


@pytest.fixture()
def common_user():
    user = User.objects.create_user(username="test_user", password="A@123456")
    return user
