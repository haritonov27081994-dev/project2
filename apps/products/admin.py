from django.contrib import admin
from .models import Category, Manufacturer, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'website')
    list_filter = ('country',)
    search_fields = ('name', 'country')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'manufacturer', 'seller', 'price', 'status', 'created_at')
    list_filter = ('status', 'category', 'manufacturer', 'created_at')
    search_fields = ('title', 'description', 'seller__username', 'manufacturer__name')
    list_editable = ('status',)
    fields = ('seller', 'category', 'manufacturer', 'title', 'description', 'price', 'image', 'status')
