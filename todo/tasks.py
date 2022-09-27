from celery import shared_task
from .models import Task
import requests
from django.core.cache import cache


@shared_task
def remove_completed_tasks():
    Task.objects.filter(completed=True).delete()


@shared_task
def check_weather():
    response = requests.get(
        "https://fd99998d-3122-4526-8338-6b73d7c9d79a.mock.pstmn.io/weather"
    )
    cache.set(
        "weather", response.json(), timeout=1500
    )  # time out is 25 minutes but will be overwritten every 20 minutes
    return cache.get("weather")
