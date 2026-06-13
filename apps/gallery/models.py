from django.db import models
from django.utils.text import slugify

from apps.core.models import PublishedModel
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
    image = models.ImageField(upload_to="gallery/%Y/%m/", validators=[validate_image_file])
    alt_text = models.CharField(max_length=180)
    caption = models.CharField(max_length=240, blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta(PublishedModel.Meta):
        verbose_name = "Gallery image"
        verbose_name_plural = "Gallery images"

    def __str__(self):
        return self.title
