from django.core.exceptions import ValidationError
from django.db import models

from .validators import validate_image_file


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublishedModel(TimeStampedModel):
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ["display_order", "id"]


class SEOMixin(models.Model):
    seo_title = models.CharField(max_length=160, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)

    class Meta:
        abstract = True


class SiteSetting(models.Model):
    hospital_name = models.CharField(max_length=160, default="Bibi Kaulan Ji Hospital")
    short_tagline = models.CharField(
        max_length=220,
        default="Trusted hospital care for families, OPD consultation, emergency support, and essential medical services.",
    )
    about_short = models.TextField(blank=True)
    address = models.TextField(blank=True)
    google_maps_url = models.URLField(blank=True)
    google_maps_embed_url = models.URLField(blank=True)
    main_phone = models.CharField(max_length=30, blank=True)
    emergency_phone = models.CharField(max_length=30, blank=True)
    ambulance_phone = models.CharField(max_length=30, blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    logo = models.ImageField(
        upload_to="site/%Y/%m/",
        blank=True,
        validators=[validate_image_file],
    )
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    og_image = models.ImageField(
        upload_to="site/og/%Y/%m/",
        blank=True,
        validators=[validate_image_file],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site setting"
        verbose_name_plural = "Site settings"

    def clean(self):
        if not self.pk and SiteSetting.objects.exists():
            raise ValidationError("Only one site settings record is allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.hospital_name

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if obj:
            return obj
        return cls(
            hospital_name="Bibi Kaulan Ji Hospital",
            short_tagline="Accessible medical care, OPD consultation, emergency support, and patient-first treatment on Ajnala Road, Gurdaspur.",
            about_short=(
                "Bibi Kaulan Ji Hospital is a local healthcare facility serving patients "
                "in Fatehgarh Churian and nearby areas with clear communication and accessible care."
            ),
            address="Opposite Axis Bank, Ajnala Road, Fatehgarh Churian, Gurdaspur-143602, Punjab",
            google_maps_url="https://www.google.com/maps/search/?api=1&query=Bibi+Kaulan+Ji+Hospital+Fatehgarh+Churian",
            google_maps_embed_url="https://www.google.com/maps?q=Bibi%20Kaulan%20Ji%20Hospital%20Fatehgarh%20Churian&output=embed",
            meta_title="Bibi Kaulan Ji Hospital | Hospital in Fatehgarh Churian",
            meta_description=(
                "Bibi Kaulan Ji Hospital in Fatehgarh Churian, Gurdaspur provides accessible "
                "medical consultation, emergency contact, appointment requests, and patient care on Ajnala Road."
            ),
        )


class Notice(TimeStampedModel):
    PRIORITY_CHOICES = [
        ("normal", "Normal"),
        ("important", "Important"),
        ("urgent", "Urgent"),
    ]

    title = models.CharField(max_length=160)
    message = models.TextField()
    link_text = models.CharField(max_length=80, blank=True)
    link_url = models.CharField(max_length=300, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="normal")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
