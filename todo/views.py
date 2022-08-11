from .models import Task
from django.views import View
from .forms import TaskUpdateForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView, DeleteView


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todo/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title']
    success_url = reverse_lazy('todo:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'todo/task_update.html'
    success_url = reverse_lazy('todo:task_list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskCompleteView(LoginRequiredMixin, View):
    model = Task
    success_url = reverse_lazy('todo:task_list')

    def get(self, request, *args, **kwargs):
        object_ = Task.objects.get(id=kwargs['pk'])
        object_.completed = True
        object_.save()
        return redirect(self.success_url)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('todo:task_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
