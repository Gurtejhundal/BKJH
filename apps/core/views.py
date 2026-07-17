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


def hospital_scope_filter(hospital_key):
    return Q(hospital_scope="both") | Q(hospital_scope=hospital_key)


MIRI_PIRI_PROFILE = {
    "name": "Miri Piri Mission Hospital",
    "punjabi_name": "ਮੀਰੀ ਪੀਰੀ ਮਿਸ਼ਨ ਹਸਪਤਾਲ",
    "tagline": "OPD and critical care support in Amritsar.",
    "address": "Opposite Namdhari Kanda, Amritsar-Tarn Taran Road, Antaryami Colony, Amritsar-143001, Punjab",
    "phone": "+91 98558 21107",
    "opd_hours": "OPD 9:00 AM - 5:00 PM",
    "emergency_hours": "Emergency support listed as available 24x7",
    "maps_url": "https://maps.app.goo.gl/h1oCCZ2XJcF7rKy36",
    "maps_embed_url": "https://www.google.com/maps?q=Opposite%20Namdhari%20Kanda%2C%20Tarn%20Taran%20Road%2C%20Amritsar%2C%20Punjab&output=embed",
    "instagram_url": "https://www.instagram.com/miripirihospital/",
    "logo_static": "images/miri-piri-logo.jpg",
    "theme": "miri",
}


def home(request):
    site = SiteSetting.get_solo()
    bibi_url = reverse("core:bibi_kaulan_hospital")
    miri_url = reverse("core:miri_piri_hospital")
    schema = {
        "@context": "https://schema.org",
        "@type": "MedicalOrganization",
        "name": "BKGH Hospitals",
        "url": request.build_absolute_uri(reverse("core:home")),
        "description": "BKGH Hospitals connects patients with Bibi Kaulan Ji Hospital and Miri Piri Mission Hospital.",
        "department": [
            {
                "@type": "Hospital",
                "name": site.hospital_name,
                "url": request.build_absolute_uri(bibi_url),
            },
            {
                "@type": "Hospital",
                "name": MIRI_PIRI_PROFILE["name"],
                "url": request.build_absolute_uri(miri_url),
            },
        ],
    }
    if site.main_phone:
        schema["telephone"] = site.main_phone
    return render(
        request,
        "pages/parent_landing.html",
        {
            "seo": seo(
                "BKGH Hospitals | Bibi Kaulan Ji Hospital & Miri Piri Mission Hospital",
                "BKGH Hospitals connects patients with Bibi Kaulan Ji Hospital and Miri Piri Mission Hospital for OPD timings, doctors, emergency support, services, and location details.",
                request.path,
            ),
            "parent_landing": True,
            "hospital_schema": json.dumps(schema),
            "bibi_url": bibi_url,
            "miri_url": miri_url,
            "bibi_tel": tel_url(site.main_phone),
            "bibi_emergency_tel": tel_url(site.emergency_phone),
            "miri_tel": tel_url(MIRI_PIRI_PROFILE["phone"]),
            "miri_profile": MIRI_PIRI_PROFILE,
        },
    )


def bibi_kaulan_hospital(request):
    site = SiteSetting.get_solo()
    bkjh_scope = hospital_scope_filter("bkjh")
    departments = Department.objects.filter(bkjh_scope, is_active=True, is_featured=True)[:6]
    doctors = Doctor.objects.select_related("department").filter(bkjh_scope, is_active=True).order_by("-is_featured", "display_order", "full_name")[:4]
    timings = OPDTiming.objects.select_related("department", "doctor").filter(bkjh_scope, is_active=True)[:6]
    gallery = GalleryImage.objects.select_related("category").filter(is_active=True, is_featured=True, category__is_active=True)[:6]
    services = Service.objects.filter(bkjh_scope, is_active=True, is_featured=True)[:6]
    facilities = Facility.objects.filter(bkjh_scope, is_active=True, is_featured=True)[:4]
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
            "miri_piri_url": reverse("core:miri_piri_hospital"),
        },
    )


def miri_piri_schema(request):
    return {
        "@context": "https://schema.org",
        "@type": "Hospital",
        "name": MIRI_PIRI_PROFILE["name"],
        "url": request.build_absolute_uri(reverse("core:miri_piri_hospital")),
        "telephone": MIRI_PIRI_PROFILE["phone"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": MIRI_PIRI_PROFILE["address"],
            "addressCountry": "IN",
        },
        "sameAs": [MIRI_PIRI_PROFILE["maps_url"], MIRI_PIRI_PROFILE["instagram_url"]],
    }


def miri_piri_hospital(request):
    miri_tel = tel_url(MIRI_PIRI_PROFILE["phone"])
    miri_scope = hospital_scope_filter("miri")
    departments = Department.objects.filter(miri_scope, is_active=True, is_featured=True).order_by("-hospital_scope", "display_order", "name")[:8]
    facilities = Facility.objects.filter(miri_scope, is_active=True, is_featured=True).order_by("-hospital_scope", "display_order", "title")[:6]
    services = Service.objects.filter(miri_scope, is_active=True, is_featured=True).order_by("-hospital_scope", "display_order", "title")[:8]
    doctors = Doctor.objects.select_related("department").filter(miri_scope, is_active=True).order_by("-hospital_scope", "-is_featured", "display_order", "full_name")[:6]
    quick_actions = [
        {
            "title": "Call Hospital",
            "support_text": "ਹਸਪਤਾਲ ਨੂੰ ਕਾਲ ਕਰੋ",
            "text": "Speak with staff before visiting.",
            "href": miri_tel,
            "icon": "phone",
        },
        {
            "title": "Get Directions",
            "support_text": "ਰਸਤਾ ਵੇਖੋ",
            "text": "Open the Tarn Taran Road location.",
            "href": MIRI_PIRI_PROFILE["maps_url"],
            "icon": "location",
            "external": True,
        },
        {
            "title": "OPD Hours",
            "support_text": "ਓਪੀਡੀ ਸਮਾਂ",
            "text": MIRI_PIRI_PROFILE["opd_hours"],
            "href": miri_tel,
            "icon": "clock",
        },
        {
            "title": "Instagram Updates",
            "support_text": "ਅਪਡੇਟਸ",
            "text": "View official posts and announcements.",
            "href": MIRI_PIRI_PROFILE["instagram_url"],
            "icon": "gallery",
            "external": True,
        },
    ]
    patient_support = [
        {"title": "OPD consultation", "text": "Public profile lists OPD services from 9:00 AM to 5:00 PM."},
        {"title": "Emergency support", "text": "Public listings describe hospital availability as 24 hours."},
        {"title": "Critical care", "text": "Critical care and ICU support are highlighted as core services."},
        {"title": "Speciality care", "text": "Chest & TB, ortho, urology, gynae, surgery, and critical care are listed."},
    ]
    return render(
        request,
        "pages/miri_piri.html",
        {
            "seo": seo(
                "Miri Piri Mission Hospital | Tarn Taran Road",
                "Miri Piri Mission Hospital provides OPD, emergency, critical care, specialty consultation and hospital support on Amritsar-Tarn Taran Road.",
                request.path,
                og_image="images/miri-piri-logo.jpg",
            ),
            "page_hospital": MIRI_PIRI_PROFILE,
            "hospital_schema": json.dumps(miri_piri_schema(request)),
            "services": services,
            "departments": departments,
            "facilities": facilities,
            "doctors": doctors,
            "quick_actions": quick_actions,
            "patient_support": patient_support,
            "miri_tel": miri_tel,
            "bkjh_url": reverse("core:bibi_kaulan_hospital"),
        },
    )


def hospital_schema(request, site):
    url = request.build_absolute_uri(reverse("core:bibi_kaulan_hospital"))
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
