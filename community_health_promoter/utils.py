from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_invitation_email(recipient_email):
    subject = "Invitation to Join CHP"
    html_content = render_to_string('invite_email.html', {
        'recipient_email': recipient_email,
        'invitation_message': "You are invited to join the CHP. We look forward to your participation!"
    })
    
    try:
        send_mail(
            subject=subject,
            message='Welcome up board to MamaMind.Help mothers by saving life', 
            html_message=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,  #
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        logger.info(f"Invitation email sent to {recipient_email}.")
    except Exception as e:
        logger.error(f"Failed to send invitation email to {recipient_email}. Error: {e}")
