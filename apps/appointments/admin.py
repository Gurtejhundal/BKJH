from django.contrib import admin

from .models import AppointmentRequest


@admin.action(description="Mark selected requests as contacted")
def mark_contacted(modeladmin, request, queryset):
    queryset.update(status=AppointmentRequest.STATUS_CONTACTED)


@admin.action(description="Mark selected requests as confirmed")
def mark_confirmed(modeladmin, request, queryset):
    queryset.update(status=AppointmentRequest.STATUS_CONFIRMED)


@admin.action(description="Mark selected requests as completed")
def mark_completed(modeladmin, request, queryset):
    queryset.update(status=AppointmentRequest.STATUS_COMPLETED)


@admin.action(description="Mark selected requests as cancelled")
def mark_cancelled(modeladmin, request, queryset):
    queryset.update(status=AppointmentRequest.STATUS_CANCELLED)


@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "hospital_scope", "phone", "department", "preferred_doctor", "preferred_date", "status", "created_at")
    list_display_links = ("patient_name", "phone")
    list_editable = ("status",)
    list_filter = ("hospital_scope", "status", "preferred_date", "department")
    search_fields = ("patient_name", "phone", "message", "admin_note")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    date_hierarchy = "preferred_date"
    autocomplete_fields = ("department", "preferred_doctor")
    list_per_page = 30
    save_on_top = True
    actions = (mark_contacted, mark_confirmed, mark_completed, mark_cancelled)
    fieldsets = (
        ("Patient contact", {"description": "Use this phone number for staff confirmation.", "fields": ("hospital_scope", "patient_name", "phone")}),
        ("Requested visit", {"description": "Preferred date/time is a request, not a confirmed appointment until staff updates the status.", "fields": ("department", "preferred_doctor", "preferred_date", "preferred_time_text", "message")}),
        ("Hospital follow-up", {"description": "Keep status and internal note updated so staff can track patient follow-up.", "fields": ("status", "admin_note")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )
