from django.contrib import admin

from .models import GalleryCategory, GalleryImage


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "display_order")
    list_editable = ("is_active", "display_order")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Gallery category", {"fields": ("name", "description")}),
        ("Show on website", {"fields": ("is_active", "display_order")}),
        ("Advanced", {"classes": ("collapse",), "fields": ("slug",)}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_featured", "is_active", "display_order", "created_at")
    list_editable = ("is_featured", "is_active", "display_order")
    list_filter = ("category", "is_featured", "is_active")
    search_fields = ("title", "alt_text", "caption")
    autocomplete_fields = ("category",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Image details", {"fields": ("category", "title", "image", "alt_text", "caption")}),
        ("Show on website", {"fields": ("is_featured", "is_active", "display_order")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )
