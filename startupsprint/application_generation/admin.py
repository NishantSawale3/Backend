from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    class Meta:
        model = Application
        fields = '__all__'