import json
import re

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from apps.gallery.models import GalleryImage
from apps.gallery.hospital.models import (
    AmbulanceInfo,
    Department,
    Doctor,
    EmergencyInfo,
    Facility,
    HealthCampUpdate,
    OPDTiming,
    Service,
)

from .models import Notice, PatientReview, SiteSetting


def seo(title, description, path="/", og_image="images/og/default-hospital.svg", og_image_url="", robots="index,follow"):
    return {
        "title": title,
        "description": description,
        "canonical_path": path,
        "og_image": og_image,
        "og_image_url": og_image_url,
        "robots": robots,
    }


def tel_url(phone):
    if not phone:
        return ""
    cleaned = re.sub(r"[^0-9+]", "", phone)
    return f"tel:{cleaned}"


def active_notices():
    today = timezone.localdate()
    return Notice.objects.filter(is_active=True).filter(
        Q(start_date__isnull=True) | Q(start_date__lte=today),
        Q(end_date__isnull=True) | Q(end_date__gte=today),
    )


def featured_reviews(limit=3):
    return PatientReview.objects.filter(is_active=True, is_featured=True, consent_confirmed=True)[:limit]


def home(request):
    site = SiteSetting.get_solo()
    departments = Department.objects.filter(is_active=True, is_featured=True)[:6]
    doctors = Doctor.objects.select_related("department").filter(is_active=True).order_by("-is_featured", "display_order", "full_name")[:4]
    timings = OPDTiming.objects.select_related("department", "doctor").filter(is_active=True)[:6]
    gallery = GalleryImage.objects.select_related("category").filter(is_active=True, is_featured=True, category__is_active=True)[:6]
    services = Service.objects.filter(is_active=True, is_featured=True)[:6]
    facilities = Facility.objects.filter(is_active=True, is_featured=True)[:4]
    emergency = EmergencyInfo.objects.filter(is_active=True).first()
    ambulance = AmbulanceInfo.objects.filter(is_active=True).first()
    schema = hospital_schema(request, site)
    seo_title = site.meta_title or f"{site.hospital_name} | Healthcare, OPD & Emergency Services"
    seo_description = site.meta_description or (
        f"{site.hospital_name} provides OPD consultation, emergency support, ambulance assistance, "
        "doctor information, departments, and appointment request support."
    )
    og_image_url = request.build_absolute_uri(site.og_image.url) if site.og_image else ""
    return render(
        request,
        "pages/home.html",
        {
            "seo": seo(seo_title, seo_description, request.path, og_image_url=og_image_url),
            "notices": active_notices()[:3],
            "departments": departments,
            "doctors": doctors,
            "timings": timings,
            "gallery_images": gallery,
            "services": services,
            "facilities": facilities,
            "emergency": emergency,
            "ambulance": ambulance,
            "patient_reviews": featured_reviews(),
            "hospital_schema": json.dumps(schema),
            "about_url": reverse("core:about"),
            "appointment_url": reverse("appointments:appointment"),
            "opd_url": reverse("hospital:opd_timing"),
            "doctors_url": reverse("hospital:doctors"),
            "departments_url": reverse("hospital:departments"),
            "ambulance_url": reverse("hospital:ambulance"),
            "emergency_url": reverse("hospital:emergency"),
            "contact_url": reverse("hospital:contact"),
            "gallery_url": reverse("hospital:gallery"),
            "main_tel": tel_url(site.main_phone),
            "emergency_tel": tel_url(site.emergency_phone or (emergency.emergency_phone if emergency else "")),
            "ambulance_tel": tel_url(site.ambulance_phone or (ambulance.ambulance_phone if ambulance else "")),
        },
    )


def hospital_schema(request, site):
    url = request.build_absolute_uri(reverse("core:home"))
    data = {
        "@context": "https://schema.org",
        "@type": "Hospital",
        "name": site.hospital_name,
        "url": url,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": site.address,
            "addressCountry": "IN",
        },
    }
    if site.main_phone:
        data["telephone"] = site.main_phone
    contact_points = []
    if site.emergency_phone:
        contact_points.append({"@type": "ContactPoint", "telephone": site.emergency_phone, "contactType": "emergency"})
    if site.ambulance_phone:
        contact_points.append({"@type": "ContactPoint", "telephone": site.ambulance_phone, "contactType": "ambulance"})
    if contact_points:
        data["contactPoint"] = contact_points
    if site.logo:
        data["image"] = request.build_absolute_uri(site.logo.url)
    if site.google_maps_url:
        data["sameAs"] = [site.google_maps_url]
    return data


def about(request):
    from apps.gallery.hospital.models import Facility, Service

    return render(
        request,
        "pages/about.html",
        {
            "seo": seo(
                "About | Bibi Kaulan Ji Hospital",
                "Learn about Bibi Kaulan Ji Hospital, patient care approach, facilities, and hospital services.",
                request.path,
            ),
            "services": Service.objects.filter(is_active=True, is_featured=True)[:3],
            "facilities": Facility.objects.filter(is_active=True, is_featured=True)[:3],
            "patient_reviews": featured_reviews(),
        },
    )


def privacy(request):
    return render(
        request,
        "pages/privacy.html",
        {"seo": seo("Privacy Policy | Bibi Kaulan Ji Hospital", "Privacy information for appointment requests and hospital website visitors.", request.path)},
    )


def terms(request):
    return render(
        request,
        "pages/terms.html",
        {"seo": seo("Terms | Bibi Kaulan Ji Hospital", "Basic website terms for Bibi Kaulan Ji Hospital visitors.", request.path)},
    )


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("django.contrib.sitemaps.views.sitemap"))
    content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin/",
            "Disallow: /dashboard/",
            "Disallow: /accounts/",
            f"Sitemap: {sitemap_url}",
            "",
        ]
    )
    return HttpResponse(content, content_type="text/plain")
