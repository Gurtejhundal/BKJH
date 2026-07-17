from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError

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


@admin.action(description="Publish selected items")
def mark_active(modeladmin, request, queryset):
    updated = 0
    rejected = []
    for item in queryset:
        item.is_active = True
        try:
            item.save()
        except ValidationError:
            rejected.append(str(item))
        else:
            updated += 1
    if updated:
        modeladmin.message_user(request, f"Published {updated} item(s).", messages.SUCCESS)
    if rejected:
        modeladmin.message_user(
            request,
            "Could not publish records with missing or inconsistent information: " + ", ".join(rejected),
            messages.WARNING,
        )


@admin.action(description="Hide selected items from website")
def mark_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description="Feature selected items on homepage")
def mark_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)


@admin.action(description="Remove selected items from homepage highlights")
def mark_unfeatured(modeladmin, request, queryset):
    queryset.update(is_featured=False)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "hospital_scope", "is_featured", "is_active", "display_order", "updated_at")
    list_display_links = ("name",)
    list_editable = ("is_featured", "is_active", "display_order")
    list_filter = ("hospital_scope", "is_featured", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "short_description", "detailed_description")
    ordering = ("display_order", "name")
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    list_per_page = 40
    actions = (mark_active, mark_inactive, mark_featured, mark_unfeatured)
    fieldsets = (
        ("Department details", {"description": "Choose one hospital first. Select shared only when staff have confirmed this department at both hospitals. Hospital photos belong in Gallery.", "fields": ("name", "hospital_scope", "short_description", "detailed_description", "services_list")}),
        ("Show on website", {"description": "Active departments appear publicly. Featured departments appear on the homepage.", "fields": ("is_featured", "is_active", "display_order")}),
        ("Advanced", {"classes": ("collapse",), "fields": ("slug", "icon", "seo_title", "seo_description")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "hospital_scope", "department", "specialization", "appointment_enabled", "is_featured", "is_active", "display_order")
    list_display_links = ("full_name",)
    list_editable = ("appointment_enabled", "is_featured", "is_active", "display_order")
    list_filter = ("hospital_scope", "department", "appointment_enabled", "is_featured", "is_active")
    prepopulated_fields = {"slug": ("full_name",)}
    search_fields = ("full_name", "qualification", "specialization")
    ordering = ("display_order", "full_name")
    autocomplete_fields = ("department",)
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    list_per_page = 40
    actions = (mark_active, mark_inactive, mark_featured, mark_unfeatured)
    fieldsets = (
        ("Doctor profile", {"description": "Assign the doctor to the confirmed hospital. Shared means the doctor actively serves both hospitals and must be selected intentionally.", "fields": ("full_name", "hospital_scope", "photo", "qualification", "specialization", "experience_years", "department", "short_bio")}),
        ("Built-in deployed photo", {"classes": ("collapse",), "description": "Used for approved doctor photos committed with the website. Leave empty for normal admin uploads.", "fields": ("static_photo_path",)}),
        ("OPD and appointment", {"description": "Use short readable timing text. Detailed timing rows can also be managed in OPD timings.", "fields": ("opd_days_text", "opd_time_text", "appointment_enabled")}),
        ("Show on website", {"description": "Active doctors appear publicly. Featured doctors appear on the homepage.", "fields": ("is_featured", "is_active", "display_order")}),
        ("Advanced", {"classes": ("collapse",), "fields": ("slug",)}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(OPDTiming)
class OPDTimingAdmin(admin.ModelAdmin):
    list_display = ("department", "doctor", "hospital_scope", "days", "start_time", "end_time", "is_active", "display_order")
    list_display_links = ("department", "doctor")
    list_editable = ("is_active", "display_order")
    list_filter = ("hospital_scope", "department", "doctor", "is_active")
    search_fields = ("days", "room_or_location", "notes", "doctor__full_name", "department__name")
    ordering = ("display_order", "department__name", "doctor__full_name")
    autocomplete_fields = ("department", "doctor")
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    list_per_page = 50
    actions = (mark_active, mark_inactive)
    fieldsets = (
        ("Timing entry", {"description": "Choose the hospital first and use only doctors and departments available there. Patients see active rows publicly.", "fields": ("hospital_scope", "department", "doctor", "days", "start_time", "end_time", "room_or_location")}),
        ("Admin note", {"description": "Internal schedule reference or staff note. This is not repeated in the public OPD table.", "fields": ("notes",)}),
        ("Show on website", {"description": "Turn off old rows instead of deleting if staff may need history.", "fields": ("is_active", "display_order")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "hospital_scope", "is_featured", "is_active", "display_order")
    list_display_links = ("title",)
    list_editable = ("is_featured", "is_active", "display_order")
    list_filter = ("hospital_scope", "is_featured", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "short_description", "detailed_description")
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    actions = (mark_active, mark_inactive, mark_featured, mark_unfeatured)
    fieldsets = (
        ("Service details", {"description": "Describe services in simple language patients can understand. Use Gallery for hospital photos.", "fields": ("title", "hospital_scope", "short_description", "detailed_description")}),
        ("Show on website", {"description": "Featured services appear on the homepage.", "fields": ("is_featured", "is_active", "display_order")}),
        ("Advanced", {"classes": ("collapse",), "fields": ("slug", "icon", "seo_title", "seo_description")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("title", "hospital_scope", "is_featured", "is_active", "display_order")
    list_display_links = ("title",)
    list_editable = ("is_featured", "is_active", "display_order")
    list_filter = ("hospital_scope", "is_featured", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "short_description", "detailed_description")
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    actions = (mark_active, mark_inactive, mark_featured, mark_unfeatured)
    fieldsets = (
        ("Facility details", {"description": "Use real facility details. Upload approved hospital photos in Gallery.", "fields": ("title", "hospital_scope", "short_description", "detailed_description")}),
        ("Show on website", {"description": "Featured facilities appear in homepage support sections.", "fields": ("is_featured", "is_active", "display_order")}),
        ("Advanced", {"classes": ("collapse",), "fields": ("slug", "seo_title", "seo_description")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(HealthCampUpdate)
class HealthCampUpdateAdmin(admin.ModelAdmin):
    list_display = ("title", "hospital_scope", "date", "is_active", "display_order")
    list_display_links = ("title",)
    list_editable = ("is_active", "display_order")
    list_filter = ("hospital_scope", "date", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "short_description", "detailed_description")
    date_hierarchy = "date"
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    actions = (mark_active, mark_inactive)
    fieldsets = (
        ("Update details", {"description": "Use for real health camps, announcements, or approved hospital updates.", "fields": ("title", "hospital_scope", "date", "short_description", "detailed_description", "image")}),
        ("Show on website", {"description": "Active updates can be shown publicly.", "fields": ("is_active", "display_order")}),
        ("Advanced", {"classes": ("collapse",), "fields": ("slug", "seo_title", "seo_description")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(EmergencyInfo)
class EmergencyInfoAdmin(admin.ModelAdmin):
    list_display = ("title", "hospital_scope", "emergency_phone", "availability_text", "is_active", "updated_at")
    list_display_links = ("title",)
    list_editable = ("is_active",)
    list_filter = ("hospital_scope", "is_active")
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    actions = (mark_active, mark_inactive)
    fieldsets = (
        ("Emergency information", {"description": "Keep emergency phone and instructions verified before publishing.", "fields": ("title", "hospital_scope", "emergency_phone", "availability_text", "description", "instructions", "is_active")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(AmbulanceInfo)
class AmbulanceInfoAdmin(admin.ModelAdmin):
    list_display = ("title", "hospital_scope", "ambulance_phone", "availability_text", "service_area", "is_active", "updated_at")
    list_display_links = ("title",)
    list_editable = ("is_active",)
    list_filter = ("hospital_scope", "is_active")
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    actions = (mark_active, mark_inactive)
    fieldsets = (
        ("Ambulance information", {"description": "Keep ambulance contact and service-area text practical for patients.", "fields": ("title", "hospital_scope", "ambulance_phone", "availability_text", "service_area", "description", "is_active")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )
