from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.core.models import PublishedModel, SEOMixin, TimeStampedModel
from apps.core.validators import validate_image_file


HOSPITAL_SCOPE_CHOICES = [
    ("both", "Both hospitals"),
    ("bkjh", "Bibi Kaulan Ji Hospital only"),
    ("miri", "Miri Piri Mission Hospital only"),
]


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


class Department(PublishedModel, SEOMixin):
    name = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=80, blank=True, help_text="Optional short icon label or CSS icon name.")
    short_description = models.TextField()
    detailed_description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="departments/%Y/%m/",
        blank=True,
        validators=[validate_image_file],
    )
    services_list = models.TextField(blank=True, help_text="One service per line.")
    is_featured = models.BooleanField(default=False)
    hospital_scope = models.CharField(max_length=12, choices=HOSPITAL_SCOPE_CHOICES, default="both")

    class Meta(PublishedModel.Meta):
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("hospital:department_detail", kwargs={"slug": self.slug})

    def service_items(self):
        return [line.strip() for line in self.services_list.splitlines() if line.strip()]

    def __str__(self):
        return self.name


class Doctor(PublishedModel):
    full_name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    photo = models.ImageField(upload_to="doctors/%Y/%m/", blank=True, validators=[validate_image_file])
    qualification = models.CharField(max_length=180, blank=True)
    specialization = models.CharField(max_length=160, blank=True)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True, related_name="doctors")
    short_bio = models.TextField(blank=True)
    opd_days_text = models.CharField(max_length=160, blank=True)
    opd_time_text = models.CharField(max_length=160, blank=True)
    appointment_enabled = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    hospital_scope = models.CharField(max_length=12, choices=HOSPITAL_SCOPE_CHOICES, default="both")

    class Meta(PublishedModel.Meta):
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.full_name)
        return super().save(*args, **kwargs)

    def initials(self):
        parts = [part[0] for part in self.full_name.split() if part]
        return "".join(parts[:2]).upper() or "DR"

    def __str__(self):
        return self.full_name


class OPDTiming(PublishedModel):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True, related_name="opd_timings")
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, blank=True, null=True, related_name="opd_timings")
    days = models.CharField(max_length=160)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    room_or_location = models.CharField(max_length=120, blank=True)
    notes = models.CharField(max_length=240, blank=True)
    hospital_scope = models.CharField(max_length=12, choices=HOSPITAL_SCOPE_CHOICES, default="both")

    class Meta(PublishedModel.Meta):
        verbose_name = "OPD timing"
        verbose_name_plural = "OPD timings"

    def time_range(self):
        if self.start_time and self.end_time:
            return f"{self.start_time.strftime('%I:%M %p').lstrip('0')} - {self.end_time.strftime('%I:%M %p').lstrip('0')}"
        return "Contact hospital"

    def __str__(self):
        label = self.doctor or self.department or "OPD"
        return f"{label} - {self.days}"


class Service(PublishedModel, SEOMixin):
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField()
    detailed_description = models.TextField(blank=True)
    icon = models.CharField(max_length=80, blank=True)
    image = models.ImageField(upload_to="services/%Y/%m/", blank=True, validators=[validate_image_file])
    is_featured = models.BooleanField(default=False)
    hospital_scope = models.CharField(max_length=12, choices=HOSPITAL_SCOPE_CHOICES, default="both")

    class Meta(PublishedModel.Meta):
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Facility(PublishedModel, SEOMixin):
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField()
    detailed_description = models.TextField(blank=True)
    image = models.ImageField(upload_to="facilities/%Y/%m/", blank=True, validators=[validate_image_file])
    is_featured = models.BooleanField(default=False)
    hospital_scope = models.CharField(max_length=12, choices=HOSPITAL_SCOPE_CHOICES, default="both")

    class Meta(PublishedModel.Meta):
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class HealthCampUpdate(PublishedModel, SEOMixin):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField()
    detailed_description = models.TextField(blank=True)
    date = models.DateField()
    image = models.ImageField(upload_to="updates/%Y/%m/", blank=True, validators=[validate_image_file])

    class Meta(PublishedModel.Meta):
        verbose_name = "Health camp update"
        verbose_name_plural = "Health camp updates"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("hospital:update_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class EmergencyInfo(TimeStampedModel):
    title = models.CharField(max_length=140, default="Emergency Service")
    emergency_phone = models.CharField(max_length=30, blank=True)
    availability_text = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Emergency info"
        verbose_name_plural = "Emergency info"

    def __str__(self):
        return self.title


class AmbulanceInfo(TimeStampedModel):
    title = models.CharField(max_length=140, default="Ambulance Service")
    ambulance_phone = models.CharField(max_length=30, blank=True)
    availability_text = models.CharField(max_length=160, blank=True)
    service_area = models.CharField(max_length=180, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Ambulance info"
        verbose_name_plural = "Ambulance info"

    def __str__(self):
        return self.title
