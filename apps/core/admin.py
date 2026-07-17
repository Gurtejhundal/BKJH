from django.contrib import admin

from .models import HospitalProfile, Notice, ParentSiteSetting, PatientReview, SiteSetting


admin.site.site_header = "BKGH Hospitals CMS"
admin.site.site_title = "BKGH CMS"
admin.site.index_title = "Website content management"


@admin.action(description="Publish selected items")
def mark_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Hide selected items from website")
def mark_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description="Feature selected patient reviews")
def mark_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)


@admin.action(description="Unfeature selected patient reviews")
def mark_unfeatured(modeladmin, request, queryset):
    queryset.update(is_featured=False)


class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("hospital_name", "main_phone", "emergency_phone", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    fieldsets = (
        ("Hospital name and logo", {"description": "Main public identity shown across the BKJH website.", "fields": ("hospital_name", "short_tagline", "about_short", "logo")}),
        ("Phone numbers", {"description": "Keep these numbers verified before publishing them publicly.", "fields": ("main_phone", "emergency_phone", "ambulance_phone", "whatsapp_number", "email")}),
        ("Address and map", {"description": "Use Google Maps URL for directions and embed URL for the website map frame.", "fields": ("address", "google_maps_url", "google_maps_embed_url")}),
        ("Homepage SEO", {"classes": ("collapse",), "description": "Optional search/social preview text.", "fields": ("meta_title", "meta_description", "og_image")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()


@admin.register(ParentSiteSetting)
class ParentSiteSettingAdmin(admin.ModelAdmin):
    list_display = ("brand_name", "helpdesk_phone", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    fieldsets = (
        ("Parent brand", {"description": "Content used on the main BKGH hospital selector website.", "fields": ("brand_name", "punjabi_name", "service_area_text", "motto_punjabi", "motto_english")}),
        ("Homepage hero", {"fields": ("hero_title", "hero_punjabi", "hero_description", "helpdesk_phone")}),
        ("Shared care section", {"fields": ("shared_care_title", "shared_care_description")}),
        ("Search and social preview", {"classes": ("collapse",), "fields": ("meta_title", "meta_description")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )

    def has_add_permission(self, request):
        return not ParentSiteSetting.objects.exists()


@admin.register(HospitalProfile)
class HospitalProfileAdmin(admin.ModelAdmin):
    list_display = ("hospital_name", "code", "call_phone", "main_phone", "emergency_phone", "is_active", "updated_at")
    list_display_links = ("hospital_name",)
    list_filter = ("code", "is_active")
    search_fields = ("hospital_name", "punjabi_name", "address", "main_phone", "call_phone")
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    fieldsets = (
        ("Hospital identity", {"description": "Select which hospital this profile controls, then edit its public name and logo.", "fields": ("code", "hospital_name", "punjabi_name", "short_tagline", "about_short", "logo", "static_logo_path", "is_active")}),
        ("Patient contact numbers", {"description": "Call Hospital buttons use the call phone. Other numbers remain visible in contact and emergency areas.", "fields": ("call_phone", "main_phone", "emergency_phone", "ambulance_phone", "whatsapp_number", "email")}),
        ("Hours and social", {"fields": ("opd_hours", "emergency_hours", "instagram_url")}),
        ("Address and map", {"fields": ("address", "google_maps_url", "google_maps_embed_url")}),
        ("Search and social preview", {"classes": ("collapse",), "fields": ("meta_title", "meta_description", "og_image")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "hospital_scope", "priority", "is_active", "start_date", "end_date", "created_at")
    list_display_links = ("title",)
    list_editable = ("priority", "is_active")
    list_filter = ("hospital_scope", "priority", "is_active")
    search_fields = ("title", "message")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    actions = (mark_active, mark_inactive)
    fieldsets = (
        ("Notice shown to patients", {"description": "Use only for real patient-facing announcements.", "fields": ("title", "message", "hospital_scope", "priority", "is_active")}),
        ("Optional link", {"description": "Add a link only when patients need a next step.", "fields": ("link_text", "link_url")}),
        ("Schedule", {"description": "Leave dates empty for a notice that can stay visible until manually hidden.", "fields": ("start_date", "end_date")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(PatientReview)
class PatientReviewAdmin(admin.ModelAdmin):
    list_display = ("reviewer_name", "hospital_scope", "review_type", "service_context", "rating", "consent_confirmed", "is_featured", "is_active", "display_order")
    list_display_links = ("reviewer_name",)
    list_editable = ("is_featured", "is_active", "display_order")
    list_filter = ("hospital_scope", "review_type", "consent_confirmed", "is_featured", "is_active")
    search_fields = ("reviewer_name", "service_context", "quote", "source_label")
    ordering = ("display_order", "reviewer_name")
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    list_per_page = 30
    actions = (mark_active, mark_inactive, mark_featured, mark_unfeatured)
    fieldsets = (
        ("Patient review", {"description": "Publish real patient/client-approved review content only.", "fields": ("reviewer_name", "hospital_scope", "service_context", "review_type", "quote", "video_url", "rating")}),
        ("Source and consent", {"description": "Reviews should stay hidden until consent is confirmed.", "fields": ("source_label", "source_url", "consent_confirmed")}),
        ("Show on website", {"description": "Featured active reviews appear in public review sections.", "fields": ("is_featured", "is_active", "display_order")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )
