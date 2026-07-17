from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import HOSPITAL_CODE_CHOICES, scope_contains


class AppointmentRequest(models.Model):
    STATUS_PENDING = "pending"
    STATUS_CONTACTED = "contacted"
    STATUS_CONFIRMED = "confirmed"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONTACTED, "Contacted"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    hospital_scope = models.CharField(max_length=12, choices=HOSPITAL_CODE_CHOICES, default="bkjh")

    patient_name = models.CharField(max_length=140)
    phone = models.CharField(max_length=30)
    department = models.ForeignKey(
        "hospital.Department",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="appointment_requests",
    )
    preferred_doctor = models.ForeignKey(
        "hospital.Doctor",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="appointment_requests",
    )
    preferred_date = models.DateField()
    preferred_time_text = models.CharField(max_length=120, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Appointment request"
        verbose_name_plural = "Appointment requests"

    def __str__(self):
        return f"{self.patient_name} - {self.phone}"

    def clean(self):
        errors = {}
        if self.department and not scope_contains(self.department.hospital_scope, self.hospital_scope):
            errors["department"] = "This department is not available at the selected hospital."
        if self.preferred_doctor and not scope_contains(self.preferred_doctor.hospital_scope, self.hospital_scope):
            errors["preferred_doctor"] = "This doctor is not available at the selected hospital."
        if (
            self.preferred_doctor
            and self.department
            and self.preferred_doctor.department_id not in {None, self.department_id}
        ):
            errors["preferred_doctor"] = "The selected doctor belongs to a different department."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
