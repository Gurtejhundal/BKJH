from django.shortcuts import get_object_or_404, render

from apps.appointments.forms import AppointmentRequestForm
from apps.core.views import featured_reviews, hospital_scope_filter, seo
from apps.gallery.models import GalleryCategory, GalleryImage

from .models import (
    AmbulanceInfo,
    Department,
    Doctor,
    EmergencyInfo,
    Facility,
    HealthCampUpdate,
    OPDTiming,
    Service,
)


def departments(request):
    query = request.GET.get("q", "").strip()
    items = Department.objects.filter(hospital_scope_filter("bkjh"), is_active=True)
    if query:
        items = items.filter(name__icontains=query)
    return render(
        request,
        "pages/departments.html",
        {
            "seo": seo("Departments | Bibi Kaulan Ji Hospital", "Explore departments, doctors, OPD timing, and appointment support at Bibi Kaulan Ji Hospital.", request.path),
            "departments": items,
            "query": query,
        },
    )


def department_detail(request, slug):
    department = get_object_or_404(Department.objects.filter(hospital_scope_filter("bkjh")), slug=slug, is_active=True)
    doctors = department.doctors.filter(is_active=True)
    timings = department.opd_timings.select_related("doctor").filter(is_active=True)
    title = department.seo_title or f"{department.name} Department | Bibi Kaulan Ji Hospital"
    description = department.seo_description or f"Learn about the {department.name} department, available doctors, OPD timing, and appointment support at Bibi Kaulan Ji Hospital."
    return render(
        request,
        "pages/department_detail.html",
        {
            "seo": seo(title, description, request.path),
            "department": department,
            "doctors": doctors,
            "timings": timings,
        },
    )


def doctors(request):
    department_id = request.GET.get("department")
    items = Doctor.objects.select_related("department").filter(hospital_scope_filter("bkjh"), is_active=True)
    if department_id:
        items = items.filter(department_id=department_id)
    return render(
        request,
        "pages/doctors.html",
        {
            "seo": seo("Doctors | Bibi Kaulan Ji Hospital", "Find doctor information, departments, OPD days, OPD timings, and appointment request options.", request.path),
            "doctors": items,
            "departments": Department.objects.filter(hospital_scope_filter("bkjh"), is_active=True),
            "selected_department": department_id,
            "patient_reviews": featured_reviews(),
        },
    )


def opd_timing(request):
    department_id = request.GET.get("department")
    items = OPDTiming.objects.select_related("department", "doctor").filter(hospital_scope_filter("bkjh"), is_active=True)
    if department_id:
        items = items.filter(department_id=department_id)
    return render(
        request,
        "pages/opd_timing.html",
        {
            "seo": seo("OPD Timing | Bibi Kaulan Ji Hospital", "Check OPD timings, doctor availability, departments, and appointment information for Bibi Kaulan Ji Hospital.", request.path),
            "timings": items,
            "departments": Department.objects.filter(hospital_scope_filter("bkjh"), is_active=True),
            "selected_department": department_id,
            "patient_reviews": featured_reviews(),
        },
    )


def services(request):
    return render(
        request,
        "pages/services.html",
        {
            "seo": seo("Services | Bibi Kaulan Ji Hospital", "View confirmed hospital services, OPD consultation, emergency support, and patient care information.", request.path),
            "services": Service.objects.filter(hospital_scope_filter("bkjh"), is_active=True),
            "featured_departments": Department.objects.filter(hospital_scope_filter("bkjh"), is_active=True, is_featured=True)[:4],
            "patient_reviews": featured_reviews(),
        },
    )


def facilities(request):
    return render(
        request,
        "pages/facilities.html",
        {
            "seo": seo("Facilities | Bibi Kaulan Ji Hospital", "View hospital facilities and patient support areas at Bibi Kaulan Ji Hospital.", request.path),
            "facilities": Facility.objects.filter(hospital_scope_filter("bkjh"), is_active=True),
            "featured_services": Service.objects.filter(hospital_scope_filter("bkjh"), is_active=True, is_featured=True)[:4],
            "patient_reviews": featured_reviews(),
        },
    )


def emergency(request):
    info = EmergencyInfo.objects.filter(is_active=True).first()
    return render(
        request,
        "pages/emergency.html",
        {
            "seo": seo("Emergency Service | Bibi Kaulan Ji Hospital", "Find emergency contact information, hospital location, and ambulance support details.", request.path),
            "emergency": info,
            "ambulance": AmbulanceInfo.objects.filter(is_active=True).first(),
            "timings": OPDTiming.objects.select_related("department", "doctor").filter(hospital_scope_filter("bkjh"), is_active=True)[:3],
        },
    )


def ambulance(request):
    info = AmbulanceInfo.objects.filter(is_active=True).first()
    return render(
        request,
        "pages/ambulance.html",
        {
            "seo": seo("Ambulance Service | Bibi Kaulan Ji Hospital", "Find ambulance contact information, availability notes, service area, and directions.", request.path),
            "ambulance": info,
            "emergency": EmergencyInfo.objects.filter(is_active=True).first(),
        },
    )


def gallery(request):
    category_slug = request.GET.get("category")
    images = GalleryImage.objects.select_related("category").filter(is_active=True, category__is_active=True)
    if category_slug:
        images = images.filter(category__slug=category_slug)
    return render(
        request,
        "pages/gallery.html",
        {
            "seo": seo("Gallery | Bibi Kaulan Ji Hospital", "View hospital photos, facilities, camps, and real gallery updates from Bibi Kaulan Ji Hospital.", request.path),
            "categories": GalleryCategory.objects.filter(is_active=True),
            "images": images,
            "selected_category": category_slug,
        },
    )


def contact(request):
    timings = OPDTiming.objects.select_related("department", "doctor").filter(hospital_scope_filter("bkjh"), is_active=True)[:6]
    return render(
        request,
        "pages/contact.html",
        {
            "seo": seo("Contact and Location | Bibi Kaulan Ji Hospital", "Find address, phone numbers, emergency contact, ambulance contact, OPD timing, and Google Maps directions.", request.path),
            "timings": timings,
            "patient_reviews": featured_reviews(),
        },
    )


def updates(request):
    return render(
        request,
        "pages/updates.html",
        {
            "seo": seo("Health Updates | Bibi Kaulan Ji Hospital", "Read hospital updates, health camp information, and patient notices from Bibi Kaulan Ji Hospital.", request.path),
            "updates": HealthCampUpdate.objects.filter(is_active=True),
        },
    )


def update_detail(request, slug):
    update = get_object_or_404(HealthCampUpdate, slug=slug, is_active=True)
    title = update.seo_title or f"{update.title} | Bibi Kaulan Ji Hospital"
    description = update.seo_description or update.short_description[:300]
    return render(
        request,
        "pages/update_detail.html",
        {"seo": seo(title, description, request.path), "update": update},
    )
