from django.urls import path
from .views import *

# urlpatterns = [
#     path('payment_gateway/', PaymentGateway.as_view()),
# ]

urlpatterns = [
    path('loan/<int:pk>/', LoanAPI.as_view()),
    path('pay/', start_payment, name="payment"),
    path('payment/success/', handle_payment_success, name="payment_success"),
    path('transactions/', TransactionListCreate.as_view(), name='transaction-list-create'),
]