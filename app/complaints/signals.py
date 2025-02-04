import threading

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    AcknowledgementLetter,
    AssignEngineer,
    AssignEngineeringAssistant,
    AssignTechnician,
    ChangePriority,
    ChangeStatus,
    Complaint,
    ComplaintComment,
)
from .utils import (
    engineer_assigned_email,
    engineering_assistant_assigned_email,
    send_technician_assigned_email,
)


@receiver(post_save, sender=AssignEngineer)
def engineer_assign_email_signal(sender, instance, created, **kwargs):
    if created:
        engineer_assigned_email_thread = threading.Thread(
            target=engineer_assigned_email, args=(instance,)
        )
        engineer_assigned_email_thread.start()


@receiver(post_save, sender=AssignEngineeringAssistant)
def engineering_assistant_assign_email_signal(sender, instance, created, **kwargs):
    if created:
        engineering_assistant_assigned_email_thread = threading.Thread(
            target=engineering_assistant_assigned_email, args=(instance,)
        )
        engineering_assistant_assigned_email_thread.start()


@receiver(post_save, sender=AssignTechnician)
def engineering_assistant_assign_email_signal(sender, instance, created, **kwargs):
    if created:
        send_technician_assigned_email_thread = threading.Thread(
            target=send_technician_assigned_email, args=(instance,)
        )
        send_technician_assigned_email_thread.start()
