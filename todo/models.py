from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    """
    Task model
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = "user"
