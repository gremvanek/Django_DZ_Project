from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        User.objects.create(
            email="admin@sky.pro",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
