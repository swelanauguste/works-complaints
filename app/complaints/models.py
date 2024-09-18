import os
import uuid

from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify
from users.models import User

from .utils import generate_short_id


class Zone(models.Model):
    district = models.CharField(max_length=100, blank=True)
    zone = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    

    def __str__(self):
        if self.district:
            return f"{self.district.upper()} | {self.zone.upper()}"
        return self.zone.upper()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name}"


class Complaint(models.Model):
    ref = models.CharField(max_length=10, unique=True, default=generate_short_id, editable=False)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
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
    complaint = models.TextField(blank=True, null=True)
    
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

    def filename(self):
        return os.path.basename(self.form.name)

    def __str__(self):

        return f"{self.ref} - {self.zone}"


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
        return f"{self.complaint}- {self.created_by}"


class AssignInvestigator(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, null=True)
    investigators = models.ManyToManyField(User, related_name="investigators")
    comment = models.TextField(blank=True)
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
        return f"{self.complaint.ref.upper()} assigned to {self.investigators.first()} by {self.created_by}"


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
        verbose_name_plural = "Change Statuses"

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
        verbose_name_plural = "Change Statuses"

    def __str__(self):
        return f"{self.complaint} {self.status}"


# class ComplaintComment(models.Model):
#     complaint = models.ForeignKey(
#         ComplaintInvestigator, on_delete=models.CASCADE, null=True
#     )
#     comment = models.TextField()
#     file = models.FieldFile(upload_to="complaints", null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.complaint.name


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
