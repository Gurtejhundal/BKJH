from django import forms

from apps.appointments.models import AppointmentRequest


class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = AppointmentRequest
        fields = ["status", "admin_note"]
        widgets = {
            "admin_note": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
