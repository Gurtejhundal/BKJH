import re

from django import forms
from django.utils import timezone

from apps.hospital.models import Department, Doctor

from .models import AppointmentRequest


PHONE_RE = re.compile(r"^[0-9+\-\s()]{7,20}$")


class AppointmentRequestForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True,
        label="I understand this is an appointment request and hospital staff will contact me for confirmation.",
    )
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = AppointmentRequest
        fields = [
            "patient_name",
            "phone",
            "department",
            "preferred_doctor",
            "preferred_date",
            "preferred_time_text",
            "message",
        ]
        widgets = {
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "message": forms.Textarea(attrs={"rows": 4}),
        }
        labels = {
            "patient_name": "Patient name",
            "phone": "Phone number",
            "preferred_doctor": "Preferred doctor",
            "preferred_time_text": "Preferred time or session",
            "message": "Message or reason for visit",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        self.fields["department"].queryset = Department.objects.filter(is_active=True)
        self.fields["preferred_doctor"].queryset = Doctor.objects.select_related("department").filter(is_active=True)
        self.fields["department"].empty_label = "Select department"
        self.fields["preferred_doctor"].empty_label = "Any available doctor"
        self.fields["message"].required = False
        self.fields["preferred_time_text"].required = False
        self.fields["preferred_doctor"].required = False

    def clean_preferred_doctor(self):
        doctor = self.cleaned_data.get("preferred_doctor")
        department = self.cleaned_data.get("department")
        if doctor and department and doctor.department_id != department.id:
            raise forms.ValidationError("Selected doctor is not linked to the selected department.")
        return doctor

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not PHONE_RE.match(phone):
            raise forms.ValidationError("Enter a valid phone number.")
        return phone

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data["preferred_date"]
        if preferred_date < timezone.localdate():
            raise forms.ValidationError("Preferred date cannot be in the past.")
        return preferred_date

    def clean_website(self):
        value = self.cleaned_data.get("website", "")
        if value:
            raise forms.ValidationError("Invalid submission.")
        return value
