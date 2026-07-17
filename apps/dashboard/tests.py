from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.appointments.models import AppointmentRequest


class DashboardTests(TestCase):
    def test_dashboard_requires_staff_login(self):
        response = self.client.get(reverse("dashboard:appointments"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_staff_can_update_status(self):
        user = get_user_model().objects.create_user(
            username="staff",
            password="test-password",
            is_staff=True,
        )
        appointment = AppointmentRequest.objects.create(
            patient_name="Test Patient",
            phone="+91 98765 43210",
            preferred_date=timezone.localdate() + timedelta(days=1),
        )
        self.client.force_login(user)
        response = self.client.post(
            reverse("dashboard:appointment_update", args=[appointment.id]),
            {"status": AppointmentRequest.STATUS_CONTACTED, "admin_note": "Called once"},
        )
        self.assertEqual(response.status_code, 302)
        appointment.refresh_from_db()
        self.assertEqual(appointment.status, AppointmentRequest.STATUS_CONTACTED)
        self.assertEqual(appointment.admin_note, "Called once")

    def test_admin_index_is_a_staff_only_bkgh_content_hub(self):
        user = get_user_model().objects.create_superuser(
            username="admin-user",
            password="test-password",
            email="admin@example.com",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manage both hospital websites")
        self.assertContains(response, reverse("admin:core_hospitalprofile_changelist"))
        self.assertContains(response, reverse("admin:gallery_galleryimage_changelist"))
