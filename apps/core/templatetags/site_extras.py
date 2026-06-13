import re

from django import template


register = template.Library()


@register.filter
def tel(value):
    if not value:
        return ""
    cleaned = re.sub(r"[^0-9+]", "", str(value))
    return cleaned


@register.filter
def whatsapp(value):
    if not value:
        return ""
    return re.sub(r"[^0-9]", "", str(value))


@register.filter
def splitlines_clean(value):
    if not value:
        return []
    return [line.strip() for line in str(value).splitlines() if line.strip()]
