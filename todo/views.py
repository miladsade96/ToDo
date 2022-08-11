from .models import Task
from django.views import View
from .forms import TaskUpdateForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView, DeleteView
