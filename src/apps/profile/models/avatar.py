import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from pydantic import BaseModel


class AvatarSettings: ...


class Avatar(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    profile = models.OneToOneField(
        "profile.Profile",
        on_delete=models.CASCADE,
        verbose_name=_("profile"),
    )

    # TODO: should make a function to generate default values and then remove null blank
    settings = models.JSONField(
        verbose_name=_("settings"),
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
    )
