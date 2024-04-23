from rest_framework import serializers
from .models import Loan, Transaction


class LoanSerializer(serializers.ModelSerializer):
    respose_timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Loan
        fields = '__all__'

class PaymentGatewaySerializer(serializers.Serializer):
    amount = serializers.FloatField()
    order_payment_id = serializers.CharField()
    isPaid = serializers.BooleanField(default=False)

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'