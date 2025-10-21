from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Confirmation', {'fields': ('confirmation_code', 'is_confirmed')}),
    )
    list_display = ('username', 'email', 'is_active', 'is_confirmed')
