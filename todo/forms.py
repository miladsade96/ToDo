from django.forms import ModelForm, CharField, TextInput
from .models import Task


class TaskUpdateForm(ModelForm):
    """
    Form for updating a task.
    """

    title = CharField(
        widget=TextInput(
            attrs={
                "class": "form-control-rounded-4",
                "placeholder": "Title",
                "name": "title",
            }
        ),
        label="",
    )

    class Meta:
        model = Task
        fields = ("title",)
