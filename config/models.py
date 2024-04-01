from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=100, verbose_name='Номер категории')
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

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
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'
