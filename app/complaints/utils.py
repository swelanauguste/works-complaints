import random
import string

import after_response
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags


def generate_short_id():
    length = 8  # You can adjust the length as needed
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for i in range(length))

@after_response.enable
def send_engineer_assigned_email(engineer, complaint):
    domain = Site.objects.get_current().domain
    complaint_url = reverse("detail", kwargs={"slug": complaint.slug})
    full_url = f"http://{domain}{complaint_url}"

    html_message = render_to_string(
        "complaints/emails/assign_engineer_email.html",
        {"complaint": complaint, "full_url": full_url, "engineer": engineer},
    )
    plain_message = strip_tags(html_message)

    subject = "New Complaint Assigned"
    message = plain_message
    from_email = settings.DEFAULT_FROM_EMAIL  # Replace with your email
    recipient_list = [engineer.email]
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)


@after_response.enable
def send_technician_assigned_email(technician, complaint):
    domain = Site.objects.get_current().domain
    complaint_url = reverse("detail", kwargs={"slug": complaint.slug})
    full_url = f"http://{domain}{complaint_url}"

    html_message = render_to_string(
        "complaints/emails/assign_technician_email.html",
        {"complaint": complaint, "full_url": full_url, "technician": technician},
    )
    plain_message = strip_tags(html_message)

    subject = "New Complaint Assigned"
    message = plain_message
    from_email = settings.DEFAULT_FROM_EMAIL  # Replace with your email
    recipient_list = [technician.email]
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)


@after_response.enable
def send_complaint_creation_email(complaint):
    domain = Site.objects.get_current().domain

    subject = f"New complaint created {complaint.ref}"
    complaint_url = reverse("detail", kwargs={"slug": complaint.slug})
    full_url = f"http://{domain}{complaint_url}"
    receipt_email_list = []
    receipt_email_list.append(settings.DEFAULT_FROM_EMAIL)
    if complaint.email is not None:
        print(complaint.email)
        receipt_email_list.append(complaint.email)
    html_message = render_to_string(
        "complaints/emails/new_complaint.html", {"complaint": complaint, "full_url": full_url}
    )
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        receipt_email_list,
        html_message=html_message,
    )
