from django.contrib import admin

from .models import Notice, SiteSetting


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Hospital identity", {"fields": ("hospital_name", "short_tagline", "about_short", "logo")}),
        ("Contact and location", {"fields": ("address", "google_maps_url", "google_maps_embed_url", "main_phone", "emergency_phone", "ambulance_phone", "whatsapp_number", "email")}),
        ("Homepage SEO", {"fields": ("meta_title", "meta_description", "og_image")}),
    )

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "priority", "is_active", "start_date", "end_date", "created_at")
    list_filter = ("priority", "is_active")
    search_fields = ("title", "message")
    ordering = ("-created_at",)
