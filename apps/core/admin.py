from django.contrib import admin

from .models import Notice, PatientReview, SiteSetting


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("hospital_name", "main_phone", "emergency_phone", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Hospital name and logo", {"fields": ("hospital_name", "short_tagline", "about_short", "logo")}),
        ("Phone numbers", {"fields": ("main_phone", "emergency_phone", "ambulance_phone", "whatsapp_number", "email")}),
        ("Address and map", {"fields": ("address", "google_maps_url", "google_maps_embed_url")}),
        ("Homepage SEO", {"classes": ("collapse",), "fields": ("meta_title", "meta_description", "og_image")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "priority", "is_active", "start_date", "end_date", "created_at")
    list_editable = ("priority", "is_active")
    list_filter = ("priority", "is_active")
    search_fields = ("title", "message")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Notice shown to patients", {"fields": ("title", "message", "priority", "is_active")}),
        ("Optional link", {"fields": ("link_text", "link_url")}),
        ("Schedule", {"fields": ("start_date", "end_date")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(PatientReview)
class PatientReviewAdmin(admin.ModelAdmin):
    list_display = ("reviewer_name", "review_type", "service_context", "rating", "consent_confirmed", "is_featured", "is_active", "display_order")
    list_editable = ("consent_confirmed", "is_featured", "is_active", "display_order")
    list_filter = ("review_type", "consent_confirmed", "is_featured", "is_active")
    search_fields = ("reviewer_name", "service_context", "quote", "source_label")
    ordering = ("display_order", "reviewer_name")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Patient review", {"fields": ("reviewer_name", "service_context", "review_type", "quote", "video_url", "rating")}),
        ("Source and consent", {"fields": ("source_label", "source_url", "consent_confirmed")}),
        ("Show on website", {"fields": ("is_featured", "is_active", "display_order")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )
