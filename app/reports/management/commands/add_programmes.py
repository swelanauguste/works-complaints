# Reconstruction & Rehabilitation
# Operation & Maintenance
# Rivers & Watercourse Maintenance/ Pre-hurricane/ desilting
# Bridges and Culverts
# Slope Stabilization


from django.core.management.base import BaseCommand

from ...models import Programme


class Command(BaseCommand):
    help = "Adding programmes to database."

    def handle(self, *args, **kwargs):
        PROGRAMME_LIST = [
            "Reconstruction & Rehabilitation",
            "Operation & Maintenance",
            "Rivers & Watercourse Maintenance/Pre-hurricane/desilting",
            "Bridges and Culverts",
            "Slope Stabilization",
        ]

        for programme in PROGRAMME_LIST:

            # Create or get the Programme object
            programme, created = Programme.objects.get_or_create(
                name=programme.lower().strip(),
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Programme '{programme}' added."))
            else:
                self.stdout.write(
                    self.style.WARNING(f"Programme '{programme}' already exists.")
                )

        self.stdout.write(self.style.SUCCESS("Successfully loaded programmes."))
