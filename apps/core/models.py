from django.core.exceptions import ValidationError
from django.db import models

from .validators import validate_image_file


HOSPITAL_SCOPE_CHOICES = [
    ("both", "Shared intentionally across both hospitals"),
    ("bkjh", "Bibi Kaulan Ji Hospital only"),
    ("miri", "Miri Piri Mission Hospital only"),
]

HOSPITAL_CODE_CHOICES = [
    ("bkjh", "Bibi Kaulan Ji Hospital"),
    ("miri", "Miri Piri Mission Hospital"),
]


def scope_contains(container_scope, item_scope):
    """Return whether a related record is available everywhere the item is published."""
    container_hospitals = {"bkjh", "miri"} if container_scope == "both" else {container_scope}
    item_hospitals = {"bkjh", "miri"} if item_scope == "both" else {item_scope}
    return item_hospitals.issubset(container_hospitals)


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


class ParentSiteSetting(models.Model):
    brand_name = models.CharField(max_length=120, default="BKGH Hospitals")
    punjabi_name = models.CharField(max_length=160, blank=True)
    service_area_text = models.CharField(
        max_length=220,
        default="Serving families across Fatehgarh Churian, Amritsar, and nearby areas",
    )
    motto_punjabi = models.CharField(max_length=160, blank=True)
    motto_english = models.CharField(max_length=120, default="Service is Our Duty")
    hero_title = models.CharField(
        max_length=180,
        default="Two Hospitals. One Trusted Healthcare Network.",
    )
    hero_punjabi = models.CharField(max_length=220, blank=True)
    hero_description = models.TextField(
        default=(
            "Choose the hospital you want to visit for doctors, OPD timings, "
            "services, emergency support, and location details."
        )
    )
    shared_care_title = models.CharField(
        max_length=180,
        default="A clearer way for patients to find the right hospital.",
    )
    shared_care_description = models.TextField(
        default=(
            "BKGH Hospitals helps patients choose between Bibi Kaulan Ji Hospital "
            "and Miri Piri Mission Hospital before checking services and directions."
        )
    )
    helpdesk_phone = models.CharField(max_length=30, blank=True)
    meta_title = models.CharField(
        max_length=160,
        default="BKGH Hospitals | Bibi Kaulan Ji Hospital & Miri Piri Mission Hospital",
    )
    meta_description = models.CharField(
        max_length=300,
        default=(
            "BKGH Hospitals connects patients with Bibi Kaulan Ji Hospital and "
            "Miri Piri Mission Hospital for OPD timings, doctors, emergency support, "
            "services, and location details."
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "BKGH parent website setting"
        verbose_name_plural = "BKGH parent website settings"

    def clean(self):
        if not self.pk and ParentSiteSetting.objects.exists():
            raise ValidationError("Only one parent website settings record is allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.brand_name

    @classmethod
    def get_solo(cls):
        return cls.objects.first() or cls()


class HospitalProfile(models.Model):
    code = models.CharField(max_length=12, choices=HOSPITAL_CODE_CHOICES, unique=True)
    hospital_name = models.CharField(max_length=160)
    punjabi_name = models.CharField(max_length=180, blank=True)
    short_tagline = models.CharField(max_length=240, blank=True)
    about_short = models.TextField(blank=True)
    address = models.TextField(blank=True)
    google_maps_url = models.URLField(blank=True)
    google_maps_embed_url = models.URLField(blank=True)
    main_phone = models.CharField(max_length=30, blank=True)
    call_phone = models.CharField(
        max_length=30,
        blank=True,
        help_text="Number used by public Call Hospital buttons.",
    )
    emergency_phone = models.CharField(max_length=30, blank=True)
    ambulance_phone = models.CharField(max_length=30, blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    opd_hours = models.CharField(max_length=140, blank=True)
    emergency_hours = models.CharField(max_length=160, blank=True)
    instagram_url = models.URLField(blank=True)
    logo = models.ImageField(
        upload_to="hospitals/logos/%Y/%m/",
        blank=True,
        validators=[validate_image_file],
    )
    static_logo_path = models.CharField(
        max_length=180,
        blank=True,
        help_text="Built-in logo path used when no uploaded logo is available.",
    )
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    og_image = models.ImageField(
        upload_to="hospitals/og/%Y/%m/",
        blank=True,
        validators=[validate_image_file],
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code"]
        verbose_name = "Hospital profile"
        verbose_name_plural = "Hospital profiles"

    def __str__(self):
        return self.hospital_name

    def clean(self):
        if not self.is_active:
            return
        required = {
            "address": self.address,
            "call_phone": self.call_phone,
            "google_maps_url": self.google_maps_url,
        }
        missing = [field.replace("_", " ") for field, value in required.items() if not value]
        if missing:
            raise ValidationError(
                f"Active hospital profiles require: {', '.join(missing)}."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def name(self):
        return self.hospital_name

    @property
    def tagline(self):
        return self.short_tagline

    @property
    def phone(self):
        return self.main_phone

    @property
    def maps_url(self):
        return self.google_maps_url

    @property
    def maps_embed_url(self):
        return self.google_maps_embed_url

    @property
    def logo_static(self):
        return self.static_logo_path

    @property
    def theme(self):
        return "miri" if self.code == "miri" else "bkjh"

    @classmethod
    def get_by_code(cls, code):
        profile = cls.objects.filter(code=code).first()
        if profile:
            return profile
        if code == "miri":
            return cls(
                code="miri",
                hospital_name="Miri Piri Mission Hospital",
                address="Opposite Namdhari Kanda, Amritsar-Tarn Taran Road, Antaryami Colony, Amritsar-143001, Punjab",
                main_phone="+91 98558 21107",
                call_phone="+91 98558 21107",
                google_maps_url="https://maps.app.goo.gl/h1oCCZ2XJcF7rKy36",
                static_logo_path="images/miri-piri-logo.jpg",
            )
        legacy = SiteSetting.get_solo()
        return cls(
            code="bkjh",
            hospital_name=legacy.hospital_name,
            short_tagline=legacy.short_tagline,
            about_short=legacy.about_short,
            address=legacy.address,
            google_maps_url=legacy.google_maps_url,
            google_maps_embed_url=legacy.google_maps_embed_url,
            main_phone=legacy.main_phone,
            call_phone=legacy.whatsapp_number or legacy.main_phone,
            emergency_phone=legacy.emergency_phone,
            ambulance_phone=legacy.ambulance_phone,
            whatsapp_number=legacy.whatsapp_number,
            email=legacy.email,
            static_logo_path="images/bkjh-logo.png",
            meta_title=legacy.meta_title,
            meta_description=legacy.meta_description,
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
    hospital_scope = models.CharField(max_length=12, choices=HOSPITAL_SCOPE_CHOICES, default="bkjh")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class PatientReview(PublishedModel):
    REVIEW_TYPE_CHOICES = [
        ("text", "Text"),
        ("video", "Video"),
    ]

    reviewer_name = models.CharField(max_length=120)
    service_context = models.CharField(max_length=140, blank=True)
    review_type = models.CharField(max_length=20, choices=REVIEW_TYPE_CHOICES, default="text")
    quote = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    source_label = models.CharField(max_length=120, blank=True)
    source_url = models.URLField(blank=True)
    rating = models.PositiveSmallIntegerField(blank=True, null=True, help_text="Optional 1-5 rating from a verified source.")
    consent_confirmed = models.BooleanField(default=False, help_text="Publish only after patient/client approval.")
    is_featured = models.BooleanField(default=True)
    hospital_scope = models.CharField(max_length=12, choices=HOSPITAL_SCOPE_CHOICES, default="bkjh")

    class Meta(PublishedModel.Meta):
        verbose_name = "Patient review"
        verbose_name_plural = "Patient reviews"

    def clean(self):
        if self.review_type == "video" and not self.video_url:
            raise ValidationError("Video reviews need a video URL.")
        if self.review_type == "text" and not self.quote:
            raise ValidationError("Text reviews need review text.")
        if self.rating is not None and not 1 <= self.rating <= 5:
            raise ValidationError("Rating must be between 1 and 5.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.reviewer_name
