from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import AppointmentRequest


class AppointmentRequestTests(TestCase):
    def test_valid_submission_creates_pending_request(self):
        response = self.client.post(
            reverse("appointments:appointment"),
            {
                "patient_name": "Test Patient",
                "phone": "+91 98765 43210",
                "preferred_date": (timezone.localdate() + timedelta(days=1)).isoformat(),
                "preferred_time_text": "Morning",
                "message": "Need OPD consultation",
                "consent": "on",
                "website": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        request_obj = AppointmentRequest.objects.get(patient_name="Test Patient")
        self.assertEqual(request_obj.status, AppointmentRequest.STATUS_PENDING)

    def test_past_date_is_rejected(self):
        response = self.client.post(
            reverse("appointments:appointment"),
            {
                "patient_name": "Test Patient",
                "phone": "+91 98765 43210",
                "preferred_date": (timezone.localdate() - timedelta(days=1)).isoformat(),
                "consent": "on",
                "website": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(AppointmentRequest.objects.exists())
