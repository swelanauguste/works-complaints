from django.contrib.auth.models import AbstractUser
from django.db import models


class Zone(models.Model):
    district = models.CharField(max_length=100, blank=True)
    zone = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['zone']

    def __str__(self):
        if self.district:
            return f"{self.zone.upper()} - {self.district.upper()}"
        return self.zone.upper()


class User(AbstractUser):
    ROLE_CHOICES = (
        ("clerk", "Clerk"),
        ("technician", "Technician"),
        ("assistant", "Engineering Assistant"),
        ("engineer", "Engineer"),
        ("chief engineer", "Chief Engineer"),
        ("chief engineer secretary", "Chief Engineer Secretary"),
        ("deputy chief engineer", "Deputy Chief Engineer"),
        ("deputy chief engineer secretary", "Deputy Chief Engineer Secretary"),
        ("complaints officer", "Complaints Officer"),
    )
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default="technician")
    phone = models.CharField(max_length=7, null=True, blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["username"]

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email
