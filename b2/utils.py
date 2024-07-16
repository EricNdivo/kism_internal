from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_welcome_email(email):
    subject = 'Dispatch Email'
    message = render_to_string('certificates/dispatch_email.html')
    sender_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, sender_email, recipient_list)