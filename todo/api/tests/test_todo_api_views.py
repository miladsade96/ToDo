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


@pytest.mark.django_db
class TestListAPIView:
    def test_list_tasks_anonymous_user_status(self, api_client):
        url = reverse("todo:todo_api:task_list")
        response = api_client.get(url)
        assert response.status_code == 401

    def test_list_tasks_loggen_in_user_status(self, api_client, common_user):
        url = reverse("todo:todo_api:task_list")
        api_client.force_authenticate(user=common_user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_task_anonymous_user(self, api_client):
        url = reverse("todo:todo_api:task_list")
        data = {"title": "test_task"}
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_task_logged_in_user(self, api_client, common_user):
        url = reverse("todo:todo_api:task_list")
        data = {"title": "test_task"}
        api_client.force_login(user=common_user)
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_create_task_anonymous_user_invalid_data(self, api_client):
        url = reverse("todo:todo_api:task_list")
        data = {}
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_create_task_logged_in_user_invalid_data(self, api_client, common_user):
        url = reverse("todo:todo_api:task_list")
        data = {}
        api_client.force_login(user=common_user)
        response = api_client.post(url, data)
        assert response.status_code == 400
