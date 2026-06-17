from django.contrib import admin
from .models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug': ('name',)}  #Django crea lo slug basandosi sul nome

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available', 'created_at')
    list_filter = ('available', 'category')
    list_editable = ('price', 'stock', 'available')  #possibilità di modificare la lista
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
