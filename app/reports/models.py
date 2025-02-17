from complaints.models import Complaint
from django.db import models
from django.utils import timezone
from users.models import User


class TechnicalReportDocument(models.Model):
    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.SET_NULL,
        null=True,
        related_name="technical_documents",
    )
    report_date = models.DateField(blank=True, null=True, default=timezone.now)
    # report_status = models.CharField(
    #     max_length=6, choices=[("open", "Open"), ("closed", "Closed")], default="open"
    # )
    document = models.FileField(
        upload_to="technical_report_documents/", null=True, blank=True
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="technical_documents_created_by",
        null=True,
    )

    def __str__(self):
        return f"{self.complaint}"


class EngineeringAssistantReportDocument(models.Model):
    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.SET_NULL,
        null=True,
        related_name="engineering_assistant_documents",
    )
    report_date = models.DateField(blank=True, null=True, default=timezone.now)
    # report_status = models.CharField(
    #     max_length=6, choices=[("open", "Open"), ("closed", "Closed")], default="open"
    # )
    document = models.FileField(
        upload_to="engineering_assistant_report_documents/", null=True, blank=True
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="engineer_assistant_documents_created_by",
        null=True,
    )

    def __str__(self):
        return f"{self.complaint}"


class EngineerReportDocument(models.Model):
    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.SET_NULL,
        null=True,
        related_name="engineering_documents",
    )
    report_date = models.DateField(blank=True, null=True, default=timezone.now)
    # report_status = models.CharField(
    #     max_length=6, choices=[("open", "Open"), ("closed", "Closed")], default="open"
    # )
    document = models.FileField(
        upload_to="engineer_report_documents/", null=True, blank=True
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="engineer_documents_created_by",
        null=True,
    )

    def __str__(self):
        return f"{self.complaint}"


class Programme(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()


class ComplaintReview(models.Model):
    complaint = models.ForeignKey(
        Complaint, on_delete=models.CASCADE, related_name="complaint_reviews"
    )
    date = models.DateField(blank=True, null=True, default=timezone.now)
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    APPROVAL_STATUS_CHOICES = (
        ("pending", "Pending Review"),
        ("not-approved", "Not Approved"),
        ("approved", "Approved"),
    )
    review = models.CharField(
        max_length=12, choices=APPROVAL_STATUS_CHOICES, default="pending"
    )
    programme = models.ForeignKey(
        Programme, on_delete=models.SET_NULL, null=True, blank=True
    )
    amount = models.FloatField(blank=True, null=True)
    cc = models.ManyToManyField(User)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.complaint.ref}"
