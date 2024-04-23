from django.core.cache import cache

from config.models import Category


def get_categories():
    categories = cache.get('categories')
    if categories:
        print('Категории найдены в кеше')
    else:
        print('Категории не найдены в кеше')

    if not categories:
        categories = list(Category.objects.all())
        cache.set('categories', categories, timeout=5)
    return categories
