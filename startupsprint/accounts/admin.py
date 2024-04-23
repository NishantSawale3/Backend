from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',)

class CustomeUserChangeForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = '__all__'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = CustomeUserChangeForm
    add_form = CustomUserCreationForm
    model = User

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "role", "gender", "photo", "signature", "is_active")}),
        (
            ("Permissions"),
            {
                "fields": (),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("id", "email", "first_name", "last_name", "is_active")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)