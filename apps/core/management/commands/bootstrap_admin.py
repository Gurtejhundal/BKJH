import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update the CMS administrator from environment variables."

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME", "admin").strip() or "admin"
        password = os.environ.get("ADMIN_PASSWORD", "")
        email = os.environ.get("ADMIN_EMAIL", "").strip()
        if not password:
            self.stdout.write(self.style.WARNING("ADMIN_PASSWORD is not set; CMS administrator was not changed."))
            return

        user_model = get_user_model()
        user, _ = user_model.objects.get_or_create(username=username)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        if email:
            user.email = email
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS(f'CMS administrator "{username}" is ready.'))
