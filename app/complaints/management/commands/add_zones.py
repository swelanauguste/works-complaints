import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from complaints.models import Zone

class Command(BaseCommand):
    help = "Load zone, district, and date data from a CSV file."

    def handle(self, *args, **kwargs):
        csv_file_path = "static/docs/complaints.csv"  # Path to your CSV file

        try:
            # Open the CSV file in binary mode to handle BOM
            with open(csv_file_path, mode='rb') as csvfile:
                # Read the first few bytes to check for BOM
                first_bytes = csvfile.read(4)
                # Decode and remove BOM if present
                if first_bytes.startswith(b'\xef\xbb\xbf'):
                    # Found UTF-8 BOM, seek back to position 3
                    csvfile.seek(3)
                else:
                    # No BOM detected, seek back to the beginning
                    csvfile.seek(0)

                # Open the file again with utf-8 decoding
                reader = csv.DictReader(csvfile.read().decode('utf-8').splitlines())

                # Print the CSV headers for debugging
                self.stdout.write(self.style.WARNING(f"CSV Headers: {reader.fieldnames}"))

                for row in reader:
                    try:
                        # Correct header handling if "\ufeff" is still present
                        zone_name = row.get("zone", "").strip().lower()
                        district_name = row.get("district", "").strip().lower()
                        # date_str = row.get("date", "").strip()

                        # Check if the zone and district fields are present
                        if not zone_name or not district_name:
                            self.stdout.write(self.style.ERROR(f"Missing zone or district in row: {row}. Skipping..."))
                            continue

                        # Parse and validate the date
                        # try:
                        #     complaint_date = datetime.strptime(date_str, "%d/%m/%Y").date()
                        # except ValueError:
                        #     self.stdout.write(self.style.ERROR(f"Invalid date format '{date_str}' for row: {row}. Skipping..."))
                        #     continue

                        # Create or get the zone object
                        zone, created = Zone.objects.get_or_create(
                            zone=zone_name,
                            defaults={"district": district_name},
                        )

                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(f"Zone '{zone_name}' with district '{district_name}' added.")
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f"Zone '{zone_name}' already exists.")
                            )

                    except IntegrityError:
                        self.stdout.write(
                            self.style.ERROR(f"Failed to add zone '{zone_name}' due to an integrity error.")
                        )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {csv_file_path} does not exist."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error processing file: {e}"))

        self.stdout.write(self.style.SUCCESS("Successfully loaded zone data from CSV."))
