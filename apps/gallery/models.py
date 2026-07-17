from django.db import models
from django.utils.text import slugify

from apps.core.models import HOSPITAL_SCOPE_CHOICES, PublishedModel
from apps.core.validators import validate_image_file


def unique_slug(instance, source_value):
    base = slugify(source_value)[:50] or "item"
    slug = base
    model = instance.__class__
    index = 2
    while model.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
        suffix = f"-{index}"
        slug = f"{base[:50 - len(suffix)]}{suffix}"
        index += 1
    return slug


class GalleryCategory(PublishedModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    hospital_scope = models.CharField(max_length=12, choices=HOSPITAL_SCOPE_CHOICES, default="bkjh")

    class Meta(PublishedModel.Meta):
        verbose_name = "Gallery category"
        verbose_name_plural = "Gallery categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GalleryImage(PublishedModel):
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name="images")
    title = models.CharField(max_length=140)
    image = models.ImageField(upload_to="gallery/%Y/%m/", blank=True, validators=[validate_image_file])
    static_image_path = models.CharField(
        max_length=220,
        blank=True,
        help_text="Built-in image path used for deployed gallery photos.",
    )
    alt_text = models.CharField(max_length=180)
    caption = models.CharField(max_length=240, blank=True)
    is_featured = models.BooleanField(default=False)
    hospital_scope = models.CharField(max_length=12, choices=HOSPITAL_SCOPE_CHOICES, default="bkjh")

    class Meta(PublishedModel.Meta):
        verbose_name = "Gallery image"
        verbose_name_plural = "Gallery images"

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError

        if not self.image and not self.static_image_path:
            raise ValidationError("Upload an image or provide a built-in image path.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
