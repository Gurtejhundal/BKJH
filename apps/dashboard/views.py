from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.appointments.models import AppointmentRequest
from apps.core.views import seo
from apps.gallery.hospital.models import Department

from .forms import AppointmentStatusForm


@staff_member_required
def appointment_dashboard(request):
    status = request.GET.get("status", "")
    date = request.GET.get("date", "")
    department_id = request.GET.get("department", "")
    query = request.GET.get("q", "").strip()
    appointments = AppointmentRequest.objects.select_related("department", "preferred_doctor")
    if status:
        appointments = appointments.filter(status=status)
    if date:
        appointments = appointments.filter(preferred_date=date)
    if department_id:
        appointments = appointments.filter(department_id=department_id)
    if query:
        appointments = appointments.filter(Q(patient_name__icontains=query) | Q(phone__icontains=query))
    paginator = Paginator(appointments, 20)
    page = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "dashboard/appointments.html",
        {
            "appointments": page,
            "status_choices": AppointmentRequest.STATUS_CHOICES,
            "departments": Department.objects.filter(is_active=True),
            "selected_status": status,
            "selected_date": date,
            "selected_department": department_id,
            "query": query,
            "seo": seo("Appointment Dashboard | Bibi Kaulan Ji Hospital", "Protected staff appointment dashboard.", request.path, robots="noindex,nofollow"),
            "pending_count": AppointmentRequest.objects.filter(status=AppointmentRequest.STATUS_PENDING).count(),
            "today_count": AppointmentRequest.objects.filter(preferred_date=timezone.localdate()).count(),
        },
    )


@staff_member_required
def appointment_update(request, pk):
    appointment = get_object_or_404(AppointmentRequest, pk=pk)
    if request.method != "POST":
        return redirect("dashboard:appointments")
    form = AppointmentStatusForm(request.POST, instance=appointment)
    if form.is_valid():
        form.save()
        messages.success(request, "Appointment request updated.")
    else:
        messages.error(request, "Could not update appointment request.")
    if request.headers.get("HX-Request"):
        return render(request, "dashboard/partials/appointment_row.html", {"appointment": appointment})
    return redirect("dashboard:appointments")
