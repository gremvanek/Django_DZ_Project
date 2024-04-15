from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '���������� ������������ �����������'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email address')

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        user = User.objects.get(email=email)
        group = Group.objects.get(name='����������')
        user.groups.add(group)
        user.save()
        self.stdout.write(self.style.SUCCESS(f"������������ {user.email} ������ � ������ �����������"))
