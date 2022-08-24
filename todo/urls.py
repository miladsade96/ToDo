from django.urls import path, include
from .views import TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskCompleteView

app_name = 'todo'

urlpatterns = [
    path('', TaskListView.as_view(), name='todo_list'),
    path('create/', TaskCreateView.as_view(), name='todo_create'),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='todo_update'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='todo_delete'),
    path('complete/<int:pk>/', TaskCompleteView.as_view(), name='todo_complete'),
    path('api/', include('todo.api.urls'))
]
