import random
import string

from django.conf import settings
from django.core.mail import send_mail


def generate_short_id():
    length = 8  # You can adjust the length as needed
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for i in range(length))


def send_engineer_assigned_email(engineer, complaint):
    subject = "New Complaint Assigned"
    message = f"You have been assigned a new complaint: {complaint.ref}"
    from_email = settings.DEFAULT_FROM_EMAIL  # Replace with your email
    recipient_list = [engineer.email]
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
