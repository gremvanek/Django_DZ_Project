from django.contrib import admin

from config.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'is_published', 'owner')
    list_filter = ('is_published', 'category')
    search_fields = ('name', 'category')
    actions = ['publish_products', 'unpublish_products']

    @admin.action(description="Опубликовать выбранные продукты")
    def publish_products(self, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Отменить публикацию выбранных продуктов")
    def unpublish_products(self, queryset):
        queryset.update(is_published=False)
