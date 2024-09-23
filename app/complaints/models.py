import os

from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify
from users.models import User, Zone

from .utils import generate_short_id


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name}"


class Complaint(models.Model):
    ref = models.CharField(
        max_length=10, unique=True, default=generate_short_id, editable=False
    )
    phone = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    zone = models.ForeignKey(
        Zone,
        on_delete=models.CASCADE,
        null=True,
    )
    date = models.DateField(
        null=True,
        blank=True,
        default=timezone.now,
    )
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    complaint = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="updated_by", null=True
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_by", null=True
    )
    form = models.FileField(upload_to="forms", null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.ref)
        super(Complaint, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})

    def get_contact_info(self):
        if self.email and self.phone:
            return f"{self.email} - {self.phone}"
        return f"{self.phone}"

    def __str__(self):

        return f"{self.ref.upper()} - {self.zone}"


class ComplaintComment(models.Model):
    complaint = models.ForeignKey(
        Complaint, on_delete=models.CASCADE, null=True, related_name="comments"
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.complaint.ref.upper()


class ComplaintPhoto(models.Model):
    complaint = models.ForeignKey(
        Complaint, on_delete=models.CASCADE, related_name="photos"
    )
    comment = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="complaints", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.complaint.name} - {self.complaint.zone}"


class AcknowledgementLetter(models.Model):
    complaint = models.ForeignKey(
        Complaint, on_delete=models.CASCADE, null=True, related_name="letters"
    )
    letter = models.FileField(upload_to="letters", null=True, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    class Meta:
        ordering = ["-created_at"]

    def filename(self):
        return os.path.basename(self.letter.name)

    def __str__(self):
        return f"{self.letter}"


class AssignEngineer(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, null=True)
    engineer = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="engineers", null=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.complaint.ref.upper()} assigned to {self.engineer} by {self.created_by}"


class AssignTechnician(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, null=True)
    technician = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="technicians", null=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.complaint.ref.upper()} assigned to {self.technician} by {self.created_by}"


class ChangeStatus(models.Model):
    STATUS_CHOICES = (
        ("is_open", "Open"),
        ("in_progress", "In Progress"),
        ("is_resolved", "Resolved"),
        ("is_closed", "Closed"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "change statuses"

    def __str__(self):
        return f"{self.complaint} {self.status}"


class ChangePriority(models.Model):
    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    )
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="low")
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "change priorities"

    def __str__(self):
        return f"{self.complaint} {self.status}"


# class Report(models.Model):
#     complaint = models.ForeignKey(
#         ComplaintInvestigator,
#         on_delete=models.CASCADE,
#         related_name="reports",
#         null=True,
#     )
#     comment = models.TextField()
#     file = models.FieldFile(upload_to="complaints", null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.complaint.name}- {self.investigator.investigator}"


# class ReportComment(models.Model):
#     complaint = models.ForeignKey(Report, on_delete=models.CASCADE)
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.complaint


# class ComplaintAction(models.Model):
#     STATUS_CHOICES = (
#         ("open", "Open"),
#         ("in_progress", "In Progress"),
#         ("resolved", "Resolved"),
#         ("closed", "Closed"),
#     )
#     PRIORITY_CHOICES = (
#         ("low", "Low"),
#         ("medium", "Medium"),
#         ("high", "High"),
#         ("urgent", "Urgent"),
#     )
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
#     priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="low")
#     report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True)
#     is_approved = models.BooleanField(null=True, blank=True)
#     comment = models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ["-created_at"]

#     def __str__(self):
#         return f"{self.complaint} {self.is_approved}"
