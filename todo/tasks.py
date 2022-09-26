from celery import shared_task
from .models import Task


@shared_task
def remove_completed_tasks():
    Task.objects.filter(completed=True).delete()
