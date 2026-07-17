from django.test import TestCase
from django.urls import reverse

from django.core.exceptions import ValidationError

from .models import Department, Doctor, OPDTiming


class HospitalRouteTests(TestCase):
    def test_public_hospital_pages_render(self):
        routes = [
            "hospital:departments",
            "hospital:doctors",
            "hospital:opd_timing",
            "hospital:services",
            "hospital:facilities",
            "hospital:emergency",
            "hospital:ambulance",
            "hospital:gallery",
            "hospital:contact",
            "hospital:updates",
        ]
        for name in routes:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_department_detail_renders_for_active_department(self):
        department = Department.objects.create(
            name="General Medicine",
            slug="general-medicine",
            short_description="General OPD consultation.",
            is_active=True,
        )
        response = self.client.get(reverse("hospital:department_detail", args=[department.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "General Medicine")

    def test_hospital_specific_models_default_to_bkjh(self):
        department = Department(name="Default Scope", short_description="Default hospital")
        doctor = Doctor(full_name="Dr. Default")
        timing = OPDTiming(days="Monday")

        self.assertEqual(department.hospital_scope, "bkjh")
        self.assertEqual(doctor.hospital_scope, "bkjh")
        self.assertEqual(timing.hospital_scope, "bkjh")

    def test_doctor_rejects_department_from_other_hospital(self):
        department = Department.objects.create(
            name="Miri Department",
            short_description="Miri only",
            hospital_scope="miri",
        )
        doctor = Doctor(
            full_name="Dr. Wrong Scope",
            department=department,
            hospital_scope="bkjh",
        )

        with self.assertRaises(ValidationError):
            doctor.save()
