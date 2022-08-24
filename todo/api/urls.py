from django.urls import path
from .views import TodoListAPIView, TodoDetailApiView

app_name = "todo_api"

urlpatterns = [
    path("task-list/", TodoListAPIView.as_view(), name="task_list"),
    path("task-detail/<int:todo_id>/", TodoDetailApiView.as_view(), name="task_detail")
]
