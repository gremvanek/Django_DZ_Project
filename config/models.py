from django.db import models

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
    price = models.TextField(**NULLABLE, verbose_name='Цена')
    # category = models.CharField(max_length=100, verbose_name='Порода')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    photo = models.ImageField(upload_to='config/', **NULLABLE, verbose_name='Превью')
    created_at = models.DateField(**NULLABLE, verbose_name='Дата создания')
    updated_at = models.DateField(**NULLABLE, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
