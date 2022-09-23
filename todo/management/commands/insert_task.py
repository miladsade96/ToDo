from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from todo.models import Task
from random import choice


class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(
            username=self.fake.first_name(),
            email=self.fake.email(),
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            password="Test@123456",
        )

        for _ in range(5):
            Task.objects.create(
                user=user,
                title=self.fake.paragraph(nb_sentences=1),
                completed=choice([True, False]),
            )
