from django.contrib import admin
from .models import Disbursement
from .models import Installment

class DisbursementAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'payment_mode', 'net_disbursed_amount', 'disbursed_to_account_no')
    list_filter = ('id', 'status')


admin.site.register(Disbursement)

class InstallmentAdmin(admin.ModelAdmin):
    list_display = ('monthly_installment_amount', 'installment_expected_date')

admin.site.register(Installment)