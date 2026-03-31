import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

try:
    from colorfield.fields import ColorField
except ImportError:
    class ColorField(models.CharField):
        def __init__(self, *args, **kwargs):
            kwargs.pop("format", None)
            kwargs.setdefault("max_length", 9)
            super().__init__(*args, **kwargs)


class AvatarColors(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    color = ColorField(verbose_name=_("color"), format="hexa")

    created_at = models.DateField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )

    updated_at = models.DateField(
        auto_now=True,
        verbose_name=_("updated at"),
    )
