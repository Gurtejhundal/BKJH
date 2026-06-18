from django.test import TestCase
from django.urls import reverse

from .models import Department


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
