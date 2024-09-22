import csv
import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.models.functions import Lower
from faker import Faker

from ...models import Complaint

fake = Faker()


class Command(BaseCommand):
    help = "Load zone data from a CSV file"

    def handle(self, *args, **kwargs):
        with open(
            "static/docs/complaints.csv", newline="", encoding="utf-8"
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                complaint = Complaint(
                    name=row["complainant"].lower().strip(),
                    address=row["address"].lower().strip(),
                    phone=row["tel"].lower().strip(),
                    complaint=row["complaint"].lower().strip(),
                )
                try:
                    complaint.save()
                    self.stdout.write(
                        self.style.SUCCESS(f"Complaint {complaint.name} added")
                    )
                except IntegrityError:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Failed to add Complaint {complaint.name} due to a duplicate"
                        )
                    )

        self.stdout.write(self.style.SUCCESS("Successfully loaded data from CSV"))
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from CSV"))
