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
    list_editable = ("is_featured", "is_active", "display_order")
    list_filter = ("is_featured", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "short_description", "detailed_description")
    ordering = ("display_order", "name")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Department details", {"fields": ("name", "short_description", "detailed_description", "services_list", "image")}),
        ("Show on website", {"fields": ("is_featured", "is_active", "display_order")}),
        ("Advanced", {"classes": ("collapse",), "fields": ("slug", "icon", "seo_title", "seo_description")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "department", "specialization", "appointment_enabled", "is_featured", "is_active", "display_order")
    list_editable = ("appointment_enabled", "is_featured", "is_active", "display_order")
    list_filter = ("department", "appointment_enabled", "is_featured", "is_active")
    prepopulated_fields = {"slug": ("full_name",)}
    search_fields = ("full_name", "qualification", "specialization")
    ordering = ("display_order", "full_name")
    autocomplete_fields = ("department",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Doctor profile", {"fields": ("full_name", "photo", "qualification", "specialization", "experience_years", "department", "short_bio")}),
        ("OPD and appointment", {"fields": ("opd_days_text", "opd_time_text", "appointment_enabled")}),
        ("Show on website", {"fields": ("is_featured", "is_active", "display_order")}),
        ("Advanced", {"classes": ("collapse",), "fields": ("slug",)}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(OPDTiming)
class OPDTimingAdmin(admin.ModelAdmin):
    list_display = ("department", "doctor", "days", "start_time", "end_time", "is_active", "display_order")
    list_editable = ("is_active", "display_order")
    list_filter = ("department", "doctor", "is_active")
    search_fields = ("days", "room_or_location", "notes", "doctor__full_name", "department__name")
    ordering = ("display_order", "department__name", "doctor__full_name")
    autocomplete_fields = ("department", "doctor")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Timing entry", {"fields": ("department", "doctor", "days", "start_time", "end_time", "room_or_location")}),
        ("Admin note", {"fields": ("notes",)}),
        ("Show on website", {"fields": ("is_active", "display_order")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "is_active", "display_order")
    list_editable = ("is_featured", "is_active", "display_order")
    list_filter = ("is_featured", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "short_description", "detailed_description")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Service details", {"fields": ("title", "short_description", "detailed_description", "image")}),
        ("Show on website", {"fields": ("is_featured", "is_active", "display_order")}),
        ("Advanced", {"classes": ("collapse",), "fields": ("slug", "icon", "seo_title", "seo_description")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "is_active", "display_order")
    list_editable = ("is_featured", "is_active", "display_order")
    list_filter = ("is_featured", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "short_description", "detailed_description")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Facility details", {"fields": ("title", "short_description", "detailed_description", "image")}),
        ("Show on website", {"fields": ("is_featured", "is_active", "display_order")}),
        ("Advanced", {"classes": ("collapse",), "fields": ("slug", "seo_title", "seo_description")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(HealthCampUpdate)
class HealthCampUpdateAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "is_active", "display_order")
    list_editable = ("is_active", "display_order")
    list_filter = ("date", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "short_description", "detailed_description")
    date_hierarchy = "date"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Update details", {"fields": ("title", "date", "short_description", "detailed_description", "image")}),
        ("Show on website", {"fields": ("is_active", "display_order")}),
        ("Advanced", {"classes": ("collapse",), "fields": ("slug", "seo_title", "seo_description")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(EmergencyInfo)
class EmergencyInfoAdmin(admin.ModelAdmin):
    list_display = ("title", "emergency_phone", "availability_text", "is_active", "updated_at")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Emergency information", {"fields": ("title", "emergency_phone", "availability_text", "description", "instructions", "is_active")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(AmbulanceInfo)
class AmbulanceInfoAdmin(admin.ModelAdmin):
    list_display = ("title", "ambulance_phone", "availability_text", "service_area", "is_active", "updated_at")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Ambulance information", {"fields": ("title", "ambulance_phone", "availability_text", "service_area", "description", "is_active")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )
