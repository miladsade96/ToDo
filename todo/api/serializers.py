from ..models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    """
    Task model serializer class
    """

    class Meta:
        model = Task
        fields = ["id", "user", "title", "completed", "created_at", "updated_at"]
        read_only_fields = ["user"]
