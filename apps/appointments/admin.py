from django.contrib import admin

from .models import AppointmentRequest


@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "phone", "department", "preferred_doctor", "preferred_date", "status", "created_at")
    list_filter = ("status", "preferred_date", "department")
    search_fields = ("patient_name", "phone", "message", "admin_note")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
