from django.contrib import admin
from .models import Loan, Vendor, Transaction


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):

    class Meta:
        model = Loan
        fields = '__all__'


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):

    class Meta:
        model = Vendor
        fields = '__all__'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    class Meta:
        model = Transaction
        fields = '__all__'