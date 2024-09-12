from django.core.mail import send_mail
from django.conf import settings

def send_invitation_email(to_email):
    send_mail(
        'Invitation to Join CHP System',
        'Dear CHP, you have been invited to join the system. Please follow the instructions to complete your registration.',
        settings.DEFAULT_FROM_EMAIL,
        [to_email]
    )
