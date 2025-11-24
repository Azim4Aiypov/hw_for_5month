from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def say_hello():
    print("Hello from Celery task!")

@shared_task
def send_test_email(user_email):
    send_mail(
        'Test Email',
        'This is a test email from Celery.',
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
