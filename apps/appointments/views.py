from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.core.models import HospitalProfile
from apps.core.views import seo, tel_url

from .forms import AppointmentRequestForm


def appointment_request(request):
    requested_hospital = request.GET.get("hospital", "bkjh")
    if requested_hospital not in {"bkjh", "miri"}:
        requested_hospital = "bkjh"
    if request.method == "POST":
        requested_hospital = request.POST.get("hospital_scope", requested_hospital)
        form = AppointmentRequestForm(request.POST, hospital_code=requested_hospital)
        if form.is_valid():
            appointment = form.save()
            messages.success(
                request,
                f"Your request for {appointment.get_hospital_scope_display()} has been received. Hospital staff will contact you for confirmation.",
            )
            return redirect(f"{reverse('appointments:appointment')}?hospital={appointment.hospital_scope}")
    else:
        form = AppointmentRequestForm(
            hospital_code=requested_hospital,
            initial={"hospital_scope": requested_hospital},
        )
    appointment_hospital = HospitalProfile.get_by_code(requested_hospital)
    is_miri = requested_hospital == "miri"
    return render(
        request,
        "pages/appointment.html",
        {
            "seo": seo(
                f"Request Appointment | {appointment_hospital.hospital_name}",
                f"Request an appointment at {appointment_hospital.hospital_name}. Staff will contact you for confirmation.",
                request.path,
            ),
            "form": form,
            "appointment_hospital": appointment_hospital,
            "page_hospital": appointment_hospital if is_miri else None,
            "miri_tel": tel_url(appointment_hospital.call_phone) if is_miri else "",
            "miri_appointment_url": f"{reverse('appointments:appointment')}?hospital=miri",
        },
    )
