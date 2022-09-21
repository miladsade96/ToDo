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
@pytest.mark.django_db
def common_user():
    user = User.objects.create_user(
        username="test_user",
        email="test_user@test.com",
        password="A@123456",
        is_active=False,
    )
    user.save()
    return user


@pytest.fixture()
@pytest.mark.django_db
def active_user():
    user = User.objects.create_user(
        username="active_user",
        email="active_user@test.com",
        password="A@123456",
    )
    user.save()
    return user


@pytest.mark.django_db
class TestRegistrationAPIView:
    def test_register_user_successfully_status(self, api_client):
        url = reverse("accounts:api-v1:registration")
        data = {
            "username": "test_user",
            "email": "test_user@test.com",
            "password": "A@123456",
            "password1": "A@123456",
        }
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_common_user_fields(self, common_user):
        assert common_user.username == "test_user"
        assert common_user.email == "test_user@test.com"
        assert common_user.is_active is False
        assert common_user.id == 1

    def test_active_user_fields(self, active_user):
        assert active_user.username == "active_user"
        assert active_user.email == "active_user@test.com"
        assert active_user.is_active is True
        assert active_user.id == 1


@pytest.mark.django_db
class TestActivationAPIView:
    def test_user_activation_successfully_status(self, common_user, api_client):
        user_token = str(RefreshToken.for_user(common_user).access_token)
        url = reverse("accounts:api-v1:activation", kwargs={"token": user_token})
        response = api_client.get(url)
        assert response.status_code == 200

    def test_user_activation_invalid_token_status(self, common_user, api_client):
        user_token = str(RefreshToken.for_user(common_user).access_token)
        url = reverse("accounts:api-v1:activation", kwargs={"token": f"{user_token}1"})
        response = api_client.get(url)
        assert response.status_code == 400


@pytest.mark.django_db
class TestActivationResendAPIView:
    def test_activation_resend_successfully_status(self, api_client, common_user):
        url = reverse("accounts:api-v1:activation_resend")
        data = {"user_id": common_user.id}
        response = api_client.post(url, data)
        assert response.status_code == 200

    def test_activation_resend_user_not_found_status(self, api_client):
        url = reverse("accounts:api-v1:activation_resend")
        data = {"user_id": 10000}
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_activation_resend_already_active_user_status(
        self, api_client, active_user
    ):
        url = reverse("accounts:api-v1:activation_resend")
        data = {"user_id": active_user.id}
        response = api_client.post(url, data)
        assert response.status_code == 400


@pytest.mark.django_db
class TestChangePasswordAPIView:
    def test_change_password_successful_status(self, api_client, active_user):
        url = reverse("accounts:api-v1:change_password")
        data = {
            "old_password": "A@123456",
            "new_password": "B#7890-=",
            "new_password1": "B#7890-=",
        }
        api_client.force_login(user=active_user)
        response = api_client.put(url, data)
        assert response.status_code == 200

    def test_change_password_new_passwords_no_match_status(
        self, api_client, active_user
    ):
        url = reverse("accounts:api-v1:change_password")
        data = {
            "old_password": "A@123456",
            "new_password": "B#7890-=",
            "new_password1": "B#7890-=as",
        }
        api_client.force_login(user=active_user)
        response = api_client.put(url, data)
        assert response.status_code == 400

    def test_change_password_old_password_no_match_status(
        self, api_client, active_user
    ):
        url = reverse("accounts:api-v1:change_password")
        data = {
            "old_password": "A@12345612345",
            "new_password": "B#7890-=",
            "new_password1": "B#7890-=",
        }
        api_client.force_login(user=active_user)
        response = api_client.put(url, data)
        assert response.status_code == 400

    def test_change_password_insecure_password_status(self, api_client, active_user):
        url = reverse("accounts:api-v1:change_password")
        data = {
            "old_password": "A@123456",
            "new_password": "12345",
            "new_password1": "12345",
        }
        api_client.force_login(user=active_user)
        response = api_client.put(url, data)
        assert response.status_code == 400
