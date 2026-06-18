from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.gallery.hospital.models import Department, HealthCampUpdate


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "core:home",
            "core:about",
            "hospital:departments",
            "hospital:doctors",
            "hospital:opd_timing",
            "appointments:appointment",
            "hospital:emergency",
            "hospital:ambulance",
            "hospital:gallery",
            "hospital:services",
            "hospital:facilities",
            "hospital:contact",
            "hospital:updates",
        ]

    def location(self, item):
        return reverse(item)


class DepartmentSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Department.objects.filter(is_active=True)


class HealthUpdateSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return HealthCampUpdate.objects.filter(is_active=True)
