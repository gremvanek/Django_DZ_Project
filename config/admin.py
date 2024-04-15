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

    def publish_products(self, request, queryset):
        queryset.update(is_published=True)

    def unpublish_products(self, request, queryset):
        queryset.update(is_published=False)

    publish_products.short_description = "Опубликовать выбранные продукты"
    unpublish_products.short_description = "Отменить публикацию выбранных продуктов"
