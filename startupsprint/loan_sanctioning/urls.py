from django.urls import path
from .views import LoanSanctionView
from .views import my_view

urlpatterns = [
    path('loan-sanction/', LoanSanctionView.as_view(), name='loan-sanction'),
    path('get-csrf-token/', my_view, name='get_csrf_token'),
]