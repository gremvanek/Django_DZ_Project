import json

from django.core.management import BaseCommand

from config.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('category_data.json', 'r', encoding='utf-8') as f:
            categories_data = json.load(f)
        return categories_data

    @staticmethod
    def json_read_products():
        with open('products_data.json', 'r', encoding='utf-8') as f:
            products_data = json.load(f)
        return products_data

    def handle(self, *args, **options):
        # Удаляем все продукты
        Product.objects.all().delete()
        # Удаляем все категории
        Category.objects.all().delete()

        # Создаем списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Создаем категории
        for category_data in Command.json_read_categories():
            category_for_create.append(
                Category(
                    id=category_data['pk'],
                    name=category_data['fields']['name'],
                    description=category_data['fields']['description']
                )
            )

        Category.objects.bulk_create(category_for_create)

        # Создаем продукты
        for product_data in Command.json_read_products():
            category_id = product_data.pop('category')
            category = Category.objects.get(id=category_id)
            product_for_create.append(
                Product(
                    category=category,
                    **product_data
                )
            )

        Product.objects.bulk_create(product_for_create)

        self.stdout.write(self.style.SUCCESS('Data successfully populated.'))
