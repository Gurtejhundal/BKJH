import os
from unittest.mock import patch

from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from apps.gallery.models import GalleryCategory, GalleryImage
from apps.gallery.hospital.models import Department, Doctor, Facility, Service

from .models import HospitalProfile, ParentSiteSetting, PatientReview


class PublicRouteTests(TestCase):
    def test_core_pages_render(self):
        for name in [
            "core:home",
            "core:bibi_kaulan_hospital",
            "core:miri_piri_hospital",
            "core:about",
            "core:privacy",
            "core:terms",
            "core:robots_txt",
        ]:
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
        response = self.client.get(reverse("core:bibi_kaulan_hospital"))
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

        bkjh_response = self.client.get(reverse("core:bibi_kaulan_hospital"))
        miri_response = self.client.get(reverse("core:miri_piri_hospital"))

        self.assertIn(shared_department, bkjh_response.context["departments"])
        self.assertIn(shared_department, miri_response.context["departments"])
        self.assertIn(bkjh_department, bkjh_response.context["departments"])
        self.assertNotIn(bkjh_department, miri_response.context["departments"])
        self.assertNotIn(miri_department, bkjh_response.context["departments"])
        self.assertIn(miri_department, miri_response.context["departments"])
        self.assertIn(shared_facility, bkjh_response.context["facilities"])
        self.assertIn(shared_facility, miri_response.context["facilities"])

    def test_bkjh_call_buttons_use_the_editable_call_phone(self):
        HospitalProfile.objects.create(
            code="bkjh",
            hospital_name="Bibi Kaulan Ji Hospital",
            call_phone="+91 97805 15050",
            address="Ajnala Road, Fatehgarh Churian, Punjab",
            google_maps_url="https://maps.example.com/bkjh",
            static_logo_path="images/bkjh-logo.png",
        )
        ParentSiteSetting.objects.create(helpdesk_phone="+91 97805 15050")

        response = self.client.get(reverse("core:bibi_kaulan_hospital"))

        self.assertContains(response, 'href="tel:+919780515050"')

    def test_parent_gateway_uses_parent_navigation_and_bkjh_logo(self):
        response = self.client.get(reverse("core:home"))

        self.assertContains(response, "Two Hospitals. One Trusted Healthcare Network.")
        self.assertContains(response, "images/bkjh-logo.png")
        self.assertContains(response, 'href="#hospitals"')
        self.assertNotContains(response, 'href="/doctors/"')
        self.assertNotContains(response, 'href="/opd-timing/"')

    def test_miri_home_hides_empty_gallery_and_internal_copy(self):
        response = self.client.get(reverse("core:miri_piri_hospital"))

        self.assertNotContains(response, "Hospital Gallery")
        self.assertNotContains(response, "Gallery being prepared")
        self.assertNotContains(response, "same active")
        self.assertNotContains(response, "Information policy")

    def test_about_page_does_not_include_miri_only_content(self):
        Service.objects.create(
            title="Miri Only Service",
            short_description="Miri service",
            hospital_scope="miri",
            is_featured=True,
        )
        Facility.objects.create(
            title="Miri Only Facility",
            short_description="Miri facility",
            hospital_scope="miri",
            is_featured=True,
        )

        response = self.client.get(reverse("core:about"))

        self.assertNotContains(response, "Miri Only Service")
        self.assertNotContains(response, "Miri Only Facility")

    def test_seed_applies_requested_doctor_corrections(self):
        call_command("seed_bkjh_content", verbosity=0)

        self.assertFalse(Doctor.objects.filter(full_name="Dr. Kashish Gupta", is_active=True).exists())
        doctor = Doctor.objects.select_related("department").get(full_name="Dr. Amrita Srivastava")
        self.assertEqual(doctor.department.name, "Ophthalmology")
        self.assertEqual(doctor.specialization, "Ophthalmology")

    def test_static_gallery_photo_renders_without_media_storage(self):
        category = GalleryCategory.objects.create(
            name="Hospital Photos",
            hospital_scope="bkjh",
            is_active=True,
        )
        GalleryImage.objects.create(
            category=category,
            title="Reception",
            static_image_path="images/hospital/bkjh-gallery-reception.jpg",
            alt_text="Hospital reception",
            hospital_scope="bkjh",
            is_active=True,
            is_featured=True,
        )

        response = self.client.get(reverse("core:bibi_kaulan_hospital"))

        self.assertContains(response, "/static/images/hospital/bkjh-gallery-reception.jpg")

    def test_gallery_image_rejects_category_from_other_hospital(self):
        category = GalleryCategory.objects.create(
            name="Miri Gallery",
            hospital_scope="miri",
            is_active=True,
        )
        image = GalleryImage(
            category=category,
            title="Wrong hospital image",
            static_image_path="images/hospital/example.jpg",
            alt_text="Hospital interior",
            hospital_scope="bkjh",
        )

        with self.assertRaises(ValidationError):
            image.save()

    @patch("apps.core.management.commands.seed_bkjh_content.IS_VERCEL", True)
    def test_vercel_seed_uses_static_gallery_paths_without_media_writes(self):
        call_command("seed_bkjh_content", verbosity=0)

        image = GalleryImage.objects.get(title="Reception")
        self.assertFalse(image.image)
        self.assertEqual(
            image.static_image_path,
            "images/hospital/bkjh-gallery-reception.jpg",
        )

    def test_admin_bootstrap_uses_environment_credentials(self):
        with patch.dict(
            os.environ,
            {"ADMIN_USERNAME": "cms-admin", "ADMIN_PASSWORD": "test-bootstrap-password"},
        ):
            call_command("bootstrap_admin", verbosity=0)

        user = get_user_model().objects.get(username="cms-admin")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertIsNotNone(authenticate(username="cms-admin", password="test-bootstrap-password"))
