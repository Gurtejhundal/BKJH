from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.gallery.hospital.models import Department, Doctor

from .models import AppointmentRequest


class AppointmentRequestTests(TestCase):
    def test_valid_submission_creates_pending_request(self):
        response = self.client.post(
            reverse("appointments:appointment"),
            {
                "hospital_scope": "bkjh",
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
                "hospital_scope": "bkjh",
                "patient_name": "Test Patient",
                "phone": "+91 98765 43210",
                "preferred_date": (timezone.localdate() - timedelta(days=1)).isoformat(),
                "consent": "on",
                "website": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(AppointmentRequest.objects.exists())

    def test_miri_submission_stores_hospital_source(self):
        response = self.client.post(
            f'{reverse("appointments:appointment")}?hospital=miri',
            {
                "hospital_scope": "miri",
                "patient_name": "Miri Patient",
                "phone": "+91 98765 43210",
                "preferred_date": (timezone.localdate() + timedelta(days=1)).isoformat(),
                "preferred_time_text": "Afternoon",
                "message": "Need consultation",
                "consent": "on",
                "website": "",
            },
        )

        self.assertEqual(response.status_code, 302)
        appointment = AppointmentRequest.objects.get(patient_name="Miri Patient")
        self.assertEqual(appointment.hospital_scope, "miri")
        self.assertIn("hospital=miri", response["Location"])

    def test_miri_form_excludes_bkjh_only_doctors_and_departments(self):
        bkjh_department = Department.objects.create(
            name="BKJH Department",
            short_description="BKJH only",
            hospital_scope="bkjh",
        )
        miri_department = Department.objects.create(
            name="Miri Department",
            short_description="Miri only",
            hospital_scope="miri",
        )
        bkjh_doctor = Doctor.objects.create(
            full_name="Dr. BKJH",
            department=bkjh_department,
            hospital_scope="bkjh",
        )
        miri_doctor = Doctor.objects.create(
            full_name="Dr. Miri",
            department=miri_department,
            hospital_scope="miri",
        )

        response = self.client.get(f'{reverse("appointments:appointment")}?hospital=miri')
        form = response.context["form"]

        self.assertNotIn(bkjh_department, form.fields["department"].queryset)
        self.assertIn(miri_department, form.fields["department"].queryset)
        self.assertNotIn(bkjh_doctor, form.fields["preferred_doctor"].queryset)
        self.assertIn(miri_doctor, form.fields["preferred_doctor"].queryset)

    def test_appointment_rejects_cross_hospital_department(self):
        department = Department.objects.create(
            name="BKJH Department",
            short_description="BKJH only",
            hospital_scope="bkjh",
        )

        appointment = AppointmentRequest(
            hospital_scope="miri",
            patient_name="Wrong Hospital",
            phone="9876543210",
            department=department,
            preferred_date=timezone.localdate() + timedelta(days=1),
        )

        with self.assertRaisesMessage(ValidationError, "not available at the selected hospital"):
            appointment.save()
