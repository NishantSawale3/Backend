# Modify this function...!!

from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import send_mail
from .models import Loan, Installment

@shared_task
def send_emi_reminder_emails():
    due_date_threshold =   + timedelta(days=5)

    # Query loans with due dates within the next 5 days
    loans = Loan.objects.filter(due_date__lte=due_date_threshold, status='pending')

    for loan in loans:
        # the email body
        email_body = f'Dear {loan.customer.first_name},\n\nThis is a reminder to pay your upcoming EMI for Loan ID {loan.id} on {loan.due_date}.\n\nPlease ensure that the payment is made on time to avoid any penalties.\n\nRegards,\nStartupsprint Team'

        # Send the email
        send_mail(
            'Reminder: Upcoming EMI Payment',
            email_body,
            'kundan221195@gmail.com',
            # [loan.customer.email],
            fail_silently=False,
        )
