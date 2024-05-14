from celery import shared_task
from datetime import datetime
from django.core.mail import send_mail
from .models import User


@shared_task
def send_birthday_emails():
    today = datetime.now().date()

    # Query customers whose birthday is today
    customers = User.objects.filter(role='customer', dob__day=today.day, dob__month=today.month)

    for customer in customers:
        # the email body
        email_body = f'Dear {customer.first_name}, Startupsprint Wishes You a happy birthday!'

        # Send the email
        send_mail(
            'Happy Birthday!',
            email_body,
            'kundan221195@gmail.com',
            [customer.email],
            fail_silently=False,
        )


# Fire these 2 commands in different terminal windows

# executes the task(worker)
# celery -A startupsprint worker --loglevel=info 
        
# scheudule the task(beat)
# celery -A startupsprint beat --loglevel=info     