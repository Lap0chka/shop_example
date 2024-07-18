from django.contrib import admin
from shop.models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'price', "discount",
                    'available', 'create_at', 'update_at')
    ordering = ['title']
    list_filter = ['available', 'create_at']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    ordering = ['name']
    prepopulated_fields = {'slug': ('name',)}