from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser, Address

# Register your models here.

@admin.register(CustomUser)  #registra un modello nell'admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')  #tabella riassuntiva
    list_filter = ('role', 'is_staff', 'is_active')  #menù a tendina
    fieldsets = UserAdmin.fieldsets + (('Ruolo', {'fields': ('role',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Ruolo', {'fields': ('role',)}),)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city', 'province', 'postal_code', 'phone_number', 'is_default')
    list_filter = ('is_default', 'province')
    search_fields = ('user__username', 'address', 'city')