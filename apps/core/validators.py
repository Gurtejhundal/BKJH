from pathlib import Path

from django.core.exceptions import ValidationError


ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_IMAGE_SIZE_MB = 6


def validate_image_file(upload):
    suffix = Path(upload.name).suffix.lower()
    if suffix not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError("Upload a JPG, PNG, WEBP, or GIF image.")
    if upload.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"Image size must be {MAX_IMAGE_SIZE_MB} MB or smaller.")
