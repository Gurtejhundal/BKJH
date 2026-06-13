from django.contrib import messages
from django.shortcuts import redirect, render

from apps.core.views import seo

from .forms import AppointmentRequestForm


def appointment_request(request):
    if request.method == "POST":
        form = AppointmentRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your appointment request has been received. Hospital staff will contact you for confirmation.",
            )
            return redirect("appointments:appointment")
    else:
        form = AppointmentRequestForm()
    return render(
        request,
        "pages/appointment.html",
        {
            "seo": seo(
                "Request Appointment | Bibi Kaulan Ji Hospital",
                "Request an appointment at Bibi Kaulan Ji Hospital. Staff will contact you for confirmation.",
                request.path,
            ),
            "form": form,
        },
    )
