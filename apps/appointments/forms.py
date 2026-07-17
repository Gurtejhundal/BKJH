import re

from django import forms
from django.db.models import Q
from django.utils import timezone

from apps.gallery.hospital.models import Department, Doctor

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
            "hospital_scope",
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
            "hospital_scope": "Hospital",
            "patient_name": "Patient name",
            "phone": "Phone number",
            "preferred_doctor": "Preferred doctor",
            "preferred_time_text": "Preferred time or session",
            "message": "Message or reason for visit",
        }

    def __init__(self, *args, hospital_code="bkjh", **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        selected_hospital = hospital_code if hospital_code in {"bkjh", "miri"} else "bkjh"
        if self.is_bound:
            selected_hospital = self.data.get(self.add_prefix("hospital_scope"), selected_hospital)
        else:
            selected_hospital = self.initial.get("hospital_scope", selected_hospital)
        if selected_hospital not in {"bkjh", "miri"}:
            selected_hospital = "bkjh"
        hospital_scope = Q(hospital_scope="both") | Q(hospital_scope=selected_hospital)
        self.fields["hospital_scope"].choices = [
            ("bkjh", "Bibi Kaulan Ji Hospital - Fatehgarh Churian"),
            ("miri", "Miri Piri Mission Hospital - Amritsar"),
        ]
        self.fields["hospital_scope"].initial = selected_hospital
        self.fields["department"].queryset = Department.objects.filter(hospital_scope, is_active=True)
        self.fields["preferred_doctor"].queryset = Doctor.objects.select_related("department").filter(
            hospital_scope,
            is_active=True,
            appointment_enabled=True,
        )
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

    def clean(self):
        cleaned_data = super().clean()
        hospital = cleaned_data.get("hospital_scope")
        department = cleaned_data.get("department")
        doctor = cleaned_data.get("preferred_doctor")
        allowed_scopes = {hospital, "both"}
        if hospital and department and department.hospital_scope not in allowed_scopes:
            self.add_error("department", "This department is not available at the selected hospital.")
        if hospital and doctor and doctor.hospital_scope not in allowed_scopes:
            self.add_error("preferred_doctor", "This doctor is not available at the selected hospital.")
        return cleaned_data

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
