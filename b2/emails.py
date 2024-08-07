from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_dispatch_email(recipient_email, dispatch_records):
    subject = 'Certificate Dispatch Notification'
    html_message = render_to_string('certificates/dispatch_email.html', {'dispatch_records': dispatch_records})
    plain_message = strip_tags(html_message)
    from_email = 'lisanzatabitha@gmail.com'
    
    try:
        send_mail(
            subject,
            plain_message,
            from_email,
            [recipient_email],
            html_message=html_message,
        )
        print(f"Email sent to: {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
