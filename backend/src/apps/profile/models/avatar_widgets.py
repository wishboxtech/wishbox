import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class AvatarWidgets(models.Model):
    class WidgetType(models.TextChoices):
        FACE = "Face", _("Face")
        TOPS = "Tops", _("Tops")
        EAR = "Ear", _("Ear")
        EARRINGS = "Earrings", _("Earrings")
        EYEBROWS = "Eyebrows", _("Eyebrows")
        EYES = "Eyes", _("Eyes")
        NOSE = "Nose", _("Nose")
        GLASSES = "Glasses", _("Glasses")
        MOUTH = "Mouth", _("Mouth")
        BEARD = "Beard", _("Beard")
        CLOTHES = "Clothes", _("Clothes")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    type = models.CharField(
        max_length=10,
        choices=WidgetType.choices,
        verbose_name=_("type"),
    )

    is_premium = models.BooleanField(
        default=False,
        verbose_name=_("is premium"),
    )

    is_active = models.BooleanField(
        default=False,
        verbose_name=_("is active"),
    )

    image = models.ForeignKey(
        "storage.MediaModel",
        on_delete=models.PROTECT,
        verbose_name=_("image"),
        related_name="widget_image",
    )

    colors = models.ManyToManyField(
        "profile.AvatarColors",
        blank=True,
        related_name="widgets",
        verbose_name=_("colors"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
    )
