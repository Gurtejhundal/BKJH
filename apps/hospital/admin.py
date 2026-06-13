from django.contrib import admin

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


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "is_featured", "is_active", "display_order", "updated_at")
    list_filter = ("is_featured", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "short_description", "detailed_description")
    ordering = ("display_order", "name")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "department", "specialization", "appointment_enabled", "is_featured", "is_active", "display_order")
    list_filter = ("department", "appointment_enabled", "is_featured", "is_active")
    prepopulated_fields = {"slug": ("full_name",)}
    search_fields = ("full_name", "qualification", "specialization")
    ordering = ("display_order", "full_name")


@admin.register(OPDTiming)
class OPDTimingAdmin(admin.ModelAdmin):
    list_display = ("department", "doctor", "days", "start_time", "end_time", "is_active", "display_order")
    list_filter = ("department", "doctor", "is_active")
    search_fields = ("days", "room_or_location", "notes", "doctor__full_name", "department__name")
    ordering = ("display_order", "department__name", "doctor__full_name")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "is_active", "display_order")
    list_filter = ("is_featured", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "short_description", "detailed_description")


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "is_active", "display_order")
    list_filter = ("is_featured", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "short_description", "detailed_description")


@admin.register(HealthCampUpdate)
class HealthCampUpdateAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "is_active", "display_order")
    list_filter = ("date", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "short_description", "detailed_description")
    date_hierarchy = "date"


@admin.register(EmergencyInfo)
class EmergencyInfoAdmin(admin.ModelAdmin):
    list_display = ("title", "emergency_phone", "availability_text", "is_active", "updated_at")
    list_filter = ("is_active",)


@admin.register(AmbulanceInfo)
class AmbulanceInfoAdmin(admin.ModelAdmin):
    list_display = ("title", "ambulance_phone", "availability_text", "service_area", "is_active", "updated_at")
    list_filter = ("is_active",)
