from django.urls import reverse
from django.utils import timezone

from users.models import *


class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=100, verbose_name='Номер категории')
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название продукта')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    photo = models.ImageField(upload_to='products/%Y/%m/%d/', null=True, blank=True, verbose_name='Превью')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания', null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения', null=True)
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def increment_views(self):
        self.views += 1
        self.save()
        return self.views


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.CharField(max_length=200, unique=True, verbose_name='Slug')
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='posts/%Y/%m/%d/', verbose_name='Превью', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_list', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'

    def increment_views(self):
        self.views += 1
        self.save()
        return self.views


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version_number = models.CharField(max_length=50)
    version_name = models.CharField(max_length=100)
    is_current = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'

    @staticmethod
    def get_absolute_url():
        return reverse('version_list')
