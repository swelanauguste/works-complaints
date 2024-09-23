import csv

from complaints.models import (  # Adjust the import based on your app structure
    Complaint,
    Zone,
)
from django.core.management.base import BaseCommand
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Load complaints data from a CSV file, including zones."

    def handle(self, *args, **kwargs):
        # CSV file path
        csv_file_path = "static/docs/complaints.csv"

        try:
            # Open the CSV file with utf-8-sig encoding to handle BOM
            with open(csv_file_path, mode="rb") as csvfile:
                # Read the first few bytes to check for BOM
                first_bytes = csvfile.read(4)
                # Decode and remove BOM if present
                if first_bytes.startswith(b"\xef\xbb\xbf"):
                    # Found UTF-8 BOM, seek back to position 3
                    csvfile.seek(3)
                else:
                    # No BOM detected, seek back to the beginning
                    csvfile.seek(0)
                
                reader = csv.DictReader(csvfile.read().decode('utf-8').splitlines())


                # Check if the header matches what you expect
                headers = reader.fieldnames
                self.stdout.write(self.style.SUCCESS(f"CSV Headers: {headers}"))

                # Ensure the correct headers are present
                required_fields = [
                    "zone",
                    "district",
                    "date",
                    "complainant",
                    "address",
                    "phone",
                    "complaint",
                ]
                for field in required_fields:
                    if field not in headers:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Missing required field '{field}' in CSV file."
                            )
                        )
                        return

                for row in reader:
                    zone_name = row["zone"].strip().lower()
                    district_name = row["district"].strip().lower()

                    # Get or create the zone
                    zone, created = Zone.objects.get_or_create(
                        zone=zone_name, defaults={"district": district_name}
                    )

                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Zone '{zone_name}' created with district '{district_name}'."
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f"Zone '{zone_name}' already exists.")
                        )

                    # Create the Complaint object
                    complaint = Complaint(
                        name=row["complainant"].strip(),
                        address=row["address"].strip(),
                        phone=row["phone"].strip(),
                        complaint=row["complaint"].strip(),
                        zone=zone,  # Associate the zone with the complaint
                    )

                    # Save the complaint and handle duplicates or errors
                    try:
                        complaint.save()
                        self.stdout.write(
                            self.style.SUCCESS(f"Complaint by '{complaint}' added.")
                        )
                    except IntegrityError:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Failed to add complaint by '{complaint}' due to a duplicate."
                            )
                        )

            # Final success message
            self.stdout.write(
                self.style.SUCCESS("Successfully loaded complaints data from CSV.")
            )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File '{csv_file_path}' not found."))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f"Missing expected column in CSV: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
