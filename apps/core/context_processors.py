import json

from django.conf import settings
from django.urls import reverse

from .models import SiteSetting


def site_context(request):
    site = SiteSetting.get_solo()
    origin = getattr(settings, "SITE_URL", "") or request.build_absolute_uri("/").rstrip("/")
    schema = {
        "@context": "https://schema.org",
        "@type": "Hospital",
        "name": site.hospital_name,
        "url": origin + reverse("core:bibi_kaulan_hospital"),
    }
    if site.address:
        schema["address"] = {
            "@type": "PostalAddress",
            "streetAddress": site.address,
            "addressCountry": "IN",
        }
    if site.main_phone:
        schema["telephone"] = site.main_phone
    contact_points = []
    if site.emergency_phone:
        contact_points.append({"@type": "ContactPoint", "telephone": site.emergency_phone, "contactType": "emergency"})
    if site.ambulance_phone:
        contact_points.append({"@type": "ContactPoint", "telephone": site.ambulance_phone, "contactType": "ambulance"})
    if contact_points:
        schema["contactPoint"] = contact_points
    if site.google_maps_url:
        schema["sameAs"] = [site.google_maps_url]
    return {
        "site": site,
        "primary_phone": site.main_phone or site.emergency_phone,
        "canonical_origin": origin,
        "site_json_ld": json.dumps(schema),
    }
