from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("technician", "Technician"),
        ("assistant", "Engineering Assistant"),
        ("engineer", "Engineer"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default="technician")
    phone = models.CharField(max_length=7, null=True, blank=True)
    
    class Meta:
        ordering = ["username"]

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email