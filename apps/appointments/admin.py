from django.contrib import admin

from .models import AppointmentRequest


@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "phone", "department", "preferred_doctor", "preferred_date", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "preferred_date", "department")
    search_fields = ("patient_name", "phone", "message", "admin_note")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    date_hierarchy = "preferred_date"
    autocomplete_fields = ("department", "preferred_doctor")
    fieldsets = (
        ("Patient contact", {"fields": ("patient_name", "phone")}),
        ("Requested visit", {"fields": ("department", "preferred_doctor", "preferred_date", "preferred_time_text", "message")}),
        ("Hospital follow-up", {"fields": ("status", "admin_note")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )
