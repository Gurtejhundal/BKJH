from django.core.management.base import BaseCommand

from apps.core.models import Notice, SiteSetting
from apps.gallery.hospital.models import Department, Facility, Service


class Command(BaseCommand):
    help = "Create safe development-only draft content. Do not use as client-approved launch content."

    def handle(self, *args, **options):
        site, _ = SiteSetting.objects.get_or_create(
            defaults={
                "hospital_name": "Bibi Kaulan Ji Hospital",
                "short_tagline": "Trusted hospital care for families, OPD consultation, emergency support, and essential medical services.",
                "about_short": "Draft development content. Replace with client-approved hospital information before launch.",
            }
        )
        Notice.objects.get_or_create(
            title="Development content notice",
            defaults={
                "message": "This local site contains draft placeholders. Verify all phone numbers, timings, doctors, departments, and claims before launch.",
                "priority": "important",
            },
        )
        for name in ["General Medicine", "Emergency Support", "OPD Consultation"]:
            Department.objects.get_or_create(
                name=name,
                defaults={
                    "short_description": "Draft department placeholder. Replace with client-approved content before publishing.",
                    "detailed_description": "This placeholder is for layout testing only.",
                    "is_active": False,
                },
            )
        for title in ["OPD Consultation", "Ambulance Support"]:
            Service.objects.get_or_create(
                title=title,
                defaults={
                    "short_description": "Draft service placeholder. Publish only after client confirmation.",
                    "is_active": False,
                },
            )
        Facility.objects.get_or_create(
            title="Waiting Area",
            defaults={
                "short_description": "Draft facility placeholder. Publish only after client confirmation.",
                "is_active": False,
            },
        )
        self.stdout.write(self.style.SUCCESS(f"Development seed content ready for {site.hospital_name}."))
