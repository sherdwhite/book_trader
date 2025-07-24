"""
Management command to migrate existing users to mandatory 2FA.
This will create EmailDevices for users who don't have them.
"""

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django_otp.plugins.otp_email.models import EmailDevice


class Command(BaseCommand):
    help = "Migrate existing users to mandatory 2FA by creating EmailDevices"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without making changes",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        if dry_run:
            self.stdout.write(
                self.style.WARNING("DRY RUN MODE - No changes will be made")
            )

        # Find users without EmailDevices
        users_without_2fa = User.objects.exclude(
            id__in=EmailDevice.objects.filter(name="primary").values_list(
                "user_id", flat=True
            )
        )

        users_without_email = users_without_2fa.filter(email="")
        users_with_email = users_without_2fa.exclude(email="")

        self.stdout.write(f"Found {users_without_2fa.count()} users without 2FA:")
        self.stdout.write(
            f"  - {users_without_email.count()} users without email addresses"
        )
        self.stdout.write(f"  - {users_with_email.count()} users with email addresses")

        if users_without_email.exists():
            self.stdout.write(self.style.WARNING("\nUsers without email addresses:"))
            for user in users_without_email:
                self.stdout.write(f"  - {user.username} (ID: {user.id})")
            self.stdout.write(
                self.style.WARNING(
                    "These users will need to add email addresses before they can log in."
                )
            )

        if users_with_email.exists():
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nCreating EmailDevices for {users_with_email.count()} users:"
                )
            )

            created_count = 0
            for user in users_with_email:
                if not dry_run:
                    device, created = EmailDevice.objects.get_or_create(
                        user=user,
                        name="primary",
                        defaults={
                            "email": user.email,
                            "confirmed": True,  # Auto-confirm for existing users
                        },
                    )
                    if created:
                        created_count += 1
                        self.stdout.write(
                            f"  ✓ Created EmailDevice for {user.username}"
                        )
                    else:
                        self.stdout.write(
                            f"  - EmailDevice already exists for {user.username}"
                        )
                else:
                    self.stdout.write(
                        f"  ✓ Would create EmailDevice for {user.username} ({user.email})"
                    )
                    created_count += 1

            if not dry_run:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\nSuccessfully created {created_count} EmailDevices"
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"\nWould create {created_count} EmailDevices")
                )

        self.stdout.write("\nMigration complete!")

        if users_without_email.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"\nNote: {users_without_email.count()} users still need email addresses. "
                    "They should update their profiles in the admin interface."
                )
            )
