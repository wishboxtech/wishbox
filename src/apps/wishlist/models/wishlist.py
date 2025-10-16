import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Wishlist(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    profile = models.ForeignKey(
        "profile.Profile",
        on_delete=models.CASCADE,
        verbose_name=_("profile"),
        related_name="wishlist",
    )

    name = models.CharField(
        max_length=150,
        verbose_name=_("name"),
    )

    description = models.TextField(
        verbose_name=_("description"),
    )

    cover = models.ForeignKey(
        "storage.MediaModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("cover"),
        related_name="wishlist_cover",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
    )
