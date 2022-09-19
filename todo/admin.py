from django.contrib import admin
from .models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at", "updated_at", "completed")
    list_filter = ("completed",)
    search_fields = ("title",)
    ordering = ("-created_at",)
    fields = ("title", "completed")
