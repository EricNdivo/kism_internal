from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_welcome_email(email):
    subject = 'Logged in kism_admin'
    message = render_to_string('certificates/welcome_email.html')
    sender_email = 'j.ericndivo@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, sender_email, recipient_list)