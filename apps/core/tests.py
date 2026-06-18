from django.test import TestCase
from django.urls import reverse

from .models import PatientReview


class PublicRouteTests(TestCase):
    def test_core_pages_render(self):
        for name in ["core:home", "core:about", "core:privacy", "core:terms", "core:robots_txt"]:
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
