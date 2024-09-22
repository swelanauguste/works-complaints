import csv

from complaints.models import Zone
from django.core.management.base import BaseCommand

from ...models import User


class Command(BaseCommand):
    help = "Import zones, users, and roles from a CSV file, creating usernames, passwords, and assigning roles."

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "csv_file", type=str, help="The path to the CSV file to be imported"
    #     )

    def handle(self, *args, **kwargs):
        csv_file = "static/docs/complaints_users.csv"

        try:
            with open(csv_file, mode="r") as file:
                reader = csv.reader(file)
                # Skip the header if it exists
                next(reader, None)

                for row in reader:
                    zone, role, email = (
                        row[0].strip().lower(),
                        row[1].strip().lower(),
                        row[2].strip().lower(),
                    )

                    # Validate role
                    if role not in [
                        "technician",
                        "engineering assistant",
                        "engineer",
                        "chief engineer",
                        "deputy chief engineer",
                        "deputy chief engineer secretary",
                        "chief engineer secretary",
                        "complaints officer",
                    ]:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Invalid role '{role}' for {email}. Skipping."
                            )
                        )
                        continue

                    # Split email to get first and last name
                    first_name, last_name = self.split_email(email)

                    # Add or get the zone
                    zone, created = Zone.objects.get_or_create(zone=zone)
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Zone {zone} created."))
                    else:
                        self.stdout.write(
                            self.style.WARNING(f"Zone {zone} already exists. Skipping.")
                        )

                    # Generate username and password
                    username = self.generate_username(email)
                    password = "Password2024"

                    # Add or update the user
                    user, created = User.objects.update_or_create(
                        email=email,
                        defaults={
                            "username": username,
                            "first_name": first_name,
                            "last_name": last_name,
                            "zone": zone,
                            "role": role,  # Assign the role
                        },
                    )

                    if created:
                        # Set the password if the user was created
                        user.set_password(password)
                        user.save()
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"User {email} created with username {username}, password {password}, and role {role}."
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"User {email} already exists. Skipping."
                            )
                        )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {csv_file} does not exist."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error processing file: {e}"))

    def split_email(self, email):
        """Split email to extract first and last names."""
        first_part = email.split("@")[0]
        parts = first_part.split(".")

        if len(parts) >= 2:
            first_name = parts[0].capitalize()
            last_name = parts[1].capitalize()
        else:
            first_name = parts[0].capitalize()
            last_name = ""

        return first_name, last_name

    def generate_username(self, email):
        """Generate a username from the email."""
        username = email.split("@")[0]
        return username

    def generate_password(self, length=8):
        """Generate a random password."""
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for i in range(length))
