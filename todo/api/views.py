from ..models import Task
from rest_framework import generics
from .serializers import TaskSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache


class TodoListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = "todo_id"

    def get_object(self, queryset=None):
        obj = get_object_or_404(Task, pk=self.kwargs["todo_id"])
        return obj

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response({"detail": "Successfully removed."}, status=204)


class WeatherApiView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        result = cache.get("weather")
        return Response(result)
