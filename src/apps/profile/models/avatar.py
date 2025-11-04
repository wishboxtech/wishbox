import json
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from pydantic_core import ValidationError as VE

from src.apps.profile.models.settings_schema import AvatarSettings


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

    def clean(self, *args, **kwargs):
        super(Avatar, self).clean(*args, **kwargs)
        try:
            avatar_settings = json.dumps(self.settings)
            AvatarSettings.model_validate_json(avatar_settings)
        except VE as e:
            # need logs here....
            raise ValidationError(f"Settings wrong format.")
        return

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Avatar, self).save(*args, **kwargs)
