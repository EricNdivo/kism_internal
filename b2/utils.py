from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_dispatch_email(email, dispatch_records):
    subject = 'Dispatch Confirmation'
    message = render_to_string('certificates/dispatch_email.html', {'dispatch_records': dispatch_records})
    sender_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, sender_email, recipient_list)


'''from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_dispatch_confirmation_email(dispatch_records):
    subject = 'Dispatch Confirmation'
    email_body = render_to_string('certificates/dispatch_confirmation_email.html', {'dispatch_records': dispatch_records})
    sender_email = settings.EMAIL_HOST_USER
    recipient_list = [record.dispatched_to for record in dispatch_records]

    send_mail(subject, email_body, sender_email, recipient_list, fail_silently=False)'''
