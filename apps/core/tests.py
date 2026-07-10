from django.test import TestCase
from django.urls import reverse

from apps.gallery.hospital.models import Department, Facility

from .models import PatientReview


class PublicRouteTests(TestCase):
    def test_core_pages_render(self):
        for name in ["core:home", "core:miri_piri_hospital", "core:about", "core:privacy", "core:terms", "core:robots_txt"]:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_sitemap_renders(self):
        response = self.client.get(reverse("django.contrib.sitemaps.views.sitemap"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<urlset", status_code=200)

    def test_unapproved_patient_review_is_not_public(self):
        PatientReview.objects.create(
            reviewer_name="Patient",
            quote="Private review text",
            consent_confirmed=False,
            is_active=True,
            is_featured=True,
        )
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Private review text")

    def test_hospital_scoped_departments_and_facilities_render_on_correct_homepages(self):
        shared_department = Department.objects.create(
            name="Shared Department",
            short_description="Available at both hospitals.",
            is_active=True,
            is_featured=True,
            hospital_scope="both",
        )
        bkjh_department = Department.objects.create(
            name="BKJH Only Department",
            short_description="Available at BKJH only.",
            is_active=True,
            is_featured=True,
            hospital_scope="bkjh",
        )
        miri_department = Department.objects.create(
            name="Miri Only Department",
            short_description="Available at Miri only.",
            is_active=True,
            is_featured=True,
            hospital_scope="miri",
        )
        shared_facility = Facility.objects.create(
            title="Shared Facility",
            short_description="Available at both hospitals.",
            is_active=True,
            is_featured=True,
            hospital_scope="both",
        )

        bkjh_response = self.client.get(reverse("core:home"))
        miri_response = self.client.get(reverse("core:miri_piri_hospital"))

        self.assertIn(shared_department, bkjh_response.context["departments"])
        self.assertIn(shared_department, miri_response.context["departments"])
        self.assertIn(bkjh_department, bkjh_response.context["departments"])
        self.assertNotIn(bkjh_department, miri_response.context["departments"])
        self.assertNotIn(miri_department, bkjh_response.context["departments"])
        self.assertIn(miri_department, miri_response.context["departments"])
        self.assertIn(shared_facility, bkjh_response.context["facilities"])
        self.assertIn(shared_facility, miri_response.context["facilities"])
