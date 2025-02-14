import random
import string

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from users.models import User


def send_approval_email(complaint, cc_email):
    admins = User.objects.filter(role="admin")
    domain = Site.objects.get_current().domain
    complaint_url = reverse("detail", kwargs={"slug": complaint.slug})
    full_url = f"{domain}{complaint_url}"
    recipient_list = []
    for cc in cc_email:
        recipient_list.append(cc.email)
    html_message = render_to_string(
        "reports/emails/project_approval.html",
        {"complaint": complaint, "full_url": full_url},
    )
    plain_message = strip_tags(html_message)

    subject = "Project Approval"
    message = plain_message
    from_email = settings.DEFAULT_FROM_EMAIL
    # recipient_list = recipient_list
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)


def send_non_approval_email(complaint):
    domain = Site.objects.get_current().domain
    complaint_url = reverse("detail", kwargs={"slug": complaint.slug})
    full_url = f"{domain}{complaint_url}"
    recipient_list = []

    html_message = render_to_string(
        "reports/emails/project_non_approval.html",
        {"complaint": complaint, "full_url": full_url},
    )
    plain_message = strip_tags(html_message)

    subject = "Project Non-Approval"
    message = plain_message
    from_email = settings.DEFAULT_FROM_EMAIL  # Replace with your email
    # recipient_list = [technician.email]
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)

