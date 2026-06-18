from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    #classe per visualizzare gli OrderItem nella pagina dell'ordine
    model = OrderItem
    extra = 0  #serve per pulire l'interfaccia
    readonly_fields = ('product_name',  'unit_price', 'quantity')  #dati in sola lettura

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status',)
    inlines = [OrderItemInline]