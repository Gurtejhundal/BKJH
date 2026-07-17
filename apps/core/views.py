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

from .models import HospitalProfile, Notice, ParentSiteSetting, PatientReview


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


def active_notices(hospital_key="bkjh"):
    today = timezone.localdate()
    return Notice.objects.filter(hospital_scope_filter(hospital_key), is_active=True).filter(
        Q(start_date__isnull=True) | Q(start_date__lte=today),
        Q(end_date__isnull=True) | Q(end_date__gte=today),
    )


def featured_reviews(hospital_key="bkjh", limit=3):
    return PatientReview.objects.filter(
        hospital_scope_filter(hospital_key),
        is_active=True,
        is_featured=True,
        consent_confirmed=True,
    )[:limit]


def hospital_scope_filter(hospital_key):
    return Q(hospital_scope="both") | Q(hospital_scope=hospital_key)


def home(request):
    site = HospitalProfile.get_by_code("bkjh")
    miri_profile = HospitalProfile.get_by_code("miri")
    parent_settings = ParentSiteSetting.get_solo()
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
                "name": miri_profile.hospital_name,
                "url": request.build_absolute_uri(miri_url),
            },
        ],
    }
    if parent_settings.helpdesk_phone or site.call_phone:
        schema["telephone"] = parent_settings.helpdesk_phone or site.call_phone
    bibi_highlights = Service.objects.filter(
        hospital_scope_filter("bkjh"), is_active=True, is_featured=True
    ).values_list("title", flat=True)[:4]
    miri_highlights = Service.objects.filter(
        hospital_scope_filter("miri"), is_active=True, is_featured=True
    ).values_list("title", flat=True)[:4]
    return render(
        request,
        "pages/parent_landing.html",
        {
            "seo": seo(
                parent_settings.meta_title,
                parent_settings.meta_description,
                request.path,
            ),
            "parent_landing": True,
            "parent_settings": parent_settings,
            "hospital_schema": json.dumps(schema),
            "bibi_url": bibi_url,
            "miri_url": miri_url,
            "bibi_tel": tel_url(site.call_phone or site.main_phone),
            "bibi_emergency_tel": tel_url(site.emergency_phone),
            "miri_tel": tel_url(miri_profile.call_phone or miri_profile.main_phone),
            "parent_tel": tel_url(parent_settings.helpdesk_phone or site.call_phone or site.main_phone),
            "miri_profile": miri_profile,
            "bibi_highlights": bibi_highlights,
            "miri_highlights": miri_highlights,
        },
    )


def bibi_kaulan_hospital(request):
    site = HospitalProfile.get_by_code("bkjh")
    bkjh_scope = hospital_scope_filter("bkjh")
    departments = Department.objects.filter(bkjh_scope, is_active=True, is_featured=True)[:6]
    doctors = Doctor.objects.select_related("department").filter(bkjh_scope, is_active=True).order_by("-is_featured", "display_order", "full_name")[:4]
    timings = OPDTiming.objects.select_related("department", "doctor").filter(bkjh_scope, is_active=True)[:6]
    gallery = GalleryImage.objects.select_related("category").filter(
        hospital_scope_filter("bkjh"),
        is_active=True,
        is_featured=True,
        category__is_active=True,
    )[:6]
    services = Service.objects.filter(bkjh_scope, is_active=True, is_featured=True)[:6]
    facilities = Facility.objects.filter(bkjh_scope, is_active=True, is_featured=True)[:4]
    emergency = EmergencyInfo.objects.filter(hospital_scope_filter("bkjh"), is_active=True).first()
    ambulance = AmbulanceInfo.objects.filter(hospital_scope_filter("bkjh"), is_active=True).first()
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
            "notices": active_notices("bkjh")[:3],
            "departments": departments,
            "doctors": doctors,
            "timings": timings,
            "gallery_images": gallery,
            "services": services,
            "facilities": facilities,
            "emergency": emergency,
            "ambulance": ambulance,
            "patient_reviews": featured_reviews("bkjh"),
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
            "main_tel": tel_url(site.call_phone or site.main_phone),
            "emergency_tel": tel_url(site.emergency_phone or (emergency.emergency_phone if emergency else "")),
            "ambulance_tel": tel_url(site.ambulance_phone or (ambulance.ambulance_phone if ambulance else "")),
            "miri_piri_url": reverse("core:miri_piri_hospital"),
        },
    )


def miri_piri_schema(request, profile):
    return {
        "@context": "https://schema.org",
        "@type": "Hospital",
        "name": profile.hospital_name,
        "url": request.build_absolute_uri(reverse("core:miri_piri_hospital")),
        "telephone": profile.call_phone or profile.main_phone,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": profile.address,
            "addressCountry": "IN",
        },
        "sameAs": [value for value in [profile.google_maps_url, profile.instagram_url] if value],
    }


def miri_piri_hospital(request):
    miri_profile = HospitalProfile.get_by_code("miri")
    miri_tel = tel_url(miri_profile.call_phone or miri_profile.main_phone)
    miri_scope = hospital_scope_filter("miri")
    departments = Department.objects.filter(miri_scope, is_active=True, is_featured=True).order_by("-hospital_scope", "display_order", "name")[:8]
    facilities = Facility.objects.filter(miri_scope, is_active=True, is_featured=True).order_by("-hospital_scope", "display_order", "title")[:6]
    services = Service.objects.filter(miri_scope, is_active=True, is_featured=True).order_by("-hospital_scope", "display_order", "title")[:8]
    doctors = Doctor.objects.select_related("department").filter(miri_scope, is_active=True).order_by("-hospital_scope", "-is_featured", "display_order", "full_name")[:6]
    gallery = GalleryImage.objects.select_related("category").filter(
        miri_scope,
        is_active=True,
        is_featured=True,
        category__is_active=True,
    )[:6]
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
            "href": miri_profile.google_maps_url,
            "icon": "location",
            "external": True,
        },
        {
            "title": "OPD Hours",
            "support_text": "ਓਪੀਡੀ ਸਮਾਂ",
            "text": miri_profile.opd_hours or "Call the hospital to confirm OPD hours.",
            "href": miri_tel,
            "icon": "clock",
        },
        {
            "title": "Instagram Updates",
            "support_text": "ਅਪਡੇਟਸ",
            "text": "View official posts and announcements.",
            "href": miri_profile.instagram_url,
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
                miri_profile.meta_title or f"{miri_profile.hospital_name} | Hospital Information",
                miri_profile.meta_description or miri_profile.short_tagline,
                request.path,
                og_image="images/miri-piri-logo.jpg",
            ),
            "page_hospital": miri_profile,
            "hospital_schema": json.dumps(miri_piri_schema(request, miri_profile)),
            "services": services,
            "departments": departments,
            "facilities": facilities,
            "doctors": doctors,
            "gallery_images": gallery,
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
