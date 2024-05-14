from django.contrib import admin
from .models import Application

class LoanAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'user', 'aadhar_no', 'pan_no')

admin.site.register(Application)
