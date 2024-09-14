import uuid

from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from users.models import User


class Zone(models.Model):
    name = models.CharField(max_length=4, unique=True)
    district = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.district.upper()} - ({self.name.upper()})"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name}"


class Complaint(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    zone = models.ForeignKey(
        Zone,
        on_delete=models.CASCADE,
        null=True,
        help_text="Where the complaint is from",
    )
    name = models.CharField(max_length=100, help_text="Your name")
    slug = models.SlugField(
        max_length=100, help_text="Your name", unique=True, null=True, blank=True
    )
    email = models.EmailField(blank=True, null=True, help_text="Your email")
    address = models.CharField(max_length=200, help_text="Your address")
    phone = models.CharField(max_length=20, help_text="Your phone number")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )
    complaint = models.TextField(help_text="Your complaint", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.uid)
        super(Complaint, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.name} - {self.zone}"


class ComplaintInvestigator(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, null=True)
    investigator = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="investigator"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.complaint} {self.investigator}"


class ComplaintComment(models.Model):
    complaint = models.ForeignKey(
        ComplaintInvestigator, on_delete=models.CASCADE, null=True
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.complaint.name


class Report(models.Model):
    complaint = models.ForeignKey(
        ComplaintInvestigator,
        on_delete=models.CASCADE,
        related_name="reports",
        null=True,
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    def __str__(self):
        return f"{self.complaint.name}- {self.investigator.investigator}"


class ReportComment(models.Model):
    complaint = models.ForeignKey(Report, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.complaint
