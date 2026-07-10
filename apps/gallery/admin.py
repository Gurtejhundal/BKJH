from django.contrib import admin

from .models import GalleryCategory, GalleryImage


@admin.action(description="Publish selected items")
def mark_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Hide selected items from website")
def mark_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description="Feature selected gallery images")
def mark_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)


@admin.action(description="Unfeature selected gallery images")
def mark_unfeatured(modeladmin, request, queryset):
    queryset.update(is_featured=False)


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "display_order")
    list_display_links = ("name",)
    list_editable = ("is_active", "display_order")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    actions = (mark_active, mark_inactive)
    fieldsets = (
        ("Gallery category", {"description": "Use categories to keep real hospital photos organized.", "fields": ("name", "description")}),
        ("Show on website", {"description": "Inactive categories hide their public images.", "fields": ("is_active", "display_order")}),
        ("Advanced", {"classes": ("collapse",), "fields": ("slug",)}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_featured", "is_active", "display_order", "created_at")
    list_display_links = ("title",)
    list_editable = ("is_featured", "is_active", "display_order")
    list_filter = ("category", "is_featured", "is_active")
    search_fields = ("title", "alt_text", "caption")
    autocomplete_fields = ("category",)
    readonly_fields = ("created_at", "updated_at")
    save_on_top = True
    list_per_page = 40
    actions = (mark_active, mark_inactive, mark_featured, mark_unfeatured)
    fieldsets = (
        ("Image details", {"description": "Upload approved real hospital photos. Alt text should describe the image for patients using screen readers.", "fields": ("category", "title", "image", "alt_text", "caption")}),
        ("Show on website", {"description": "Featured active images can appear on the homepage/gallery highlights.", "fields": ("is_featured", "is_active", "display_order")}),
        ("Admin timestamps", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )
