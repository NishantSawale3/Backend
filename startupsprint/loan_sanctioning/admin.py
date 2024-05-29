from django.contrib import admin
from .models import Loan

class LoanAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'user', 'amount', 'interest', 'duration', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')

admin.site.register(Loan)
