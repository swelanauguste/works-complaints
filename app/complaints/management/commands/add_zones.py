import csv

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.models.functions import Lower

from ...models import Zone


class Command(BaseCommand):
    help = "Load zone data from a CSV file"

    def handle(self, *args, **kwargs):
        with open(
            "static/docs/complaints.csv", newline="", encoding="utf-8"
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    # Create the zone object
                    zone, created = Zone.objects.get_or_create(
                        name=row["ZONE"].lower().strip(),
                        defaults={"district": row["DISTRICT"].lower().strip()},
                    )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f"Zone {row['ZONE']} added")
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f"Zone {row['ZONE']} already exists")
                        )

                except IntegrityError:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Failed to add Zone {row['ZONE']} due to a duplicate"
                        )
                    )

        self.stdout.write(self.style.SUCCESS("Successfully loaded data from CSV"))
