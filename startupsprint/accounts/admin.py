from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm  

# Define a custom UserAdmin class to customize the admin interface
class UserAdmin(BaseUserAdmin):
    model = User
    add_form = UserCreationForm
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'dob', 'gender')}),
        ('Contact details', {'fields': ('mobile',)}),
        ('Address', {'fields': ('permanent_address', 'current_address')}),
        ('Additional info', {'fields': ('photo', 'signature', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'dob', 'gender', 'mobile','is_active', 'is_staff','role'),
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_active', 'role','is_staff')
    list_filter = ('is_active', 'role')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)  


admin.site.register(User, UserAdmin)
