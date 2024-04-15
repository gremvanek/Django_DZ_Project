from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Product


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='Модераторы')
        instance.groups.add(group)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Создание группы модераторов
moderators_group, created = Group.objects.get_or_create(name='Модераторы')

# Получение разрешений для модели Product
content_type = ContentType.objects.get_for_model(Product)
can_change_published_status = Permission.objects.get(codename='can_change_published_status', content_type=content_type)
can_change_description = Permission.objects.get(codename='can_change_description', content_type=content_type)
can_change_category = Permission.objects.get(codename='can_change_category', content_type=content_type)

# Назначение разрешений группе модераторов
moderators_group.permissions.add(can_change_published_status, can_change_description, can_change_category)
