import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Wish(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    wishlist = models.ForeignKey(
        "wishlist.Wishlist",
        on_delete=models.CASCADE,
        verbose_name=_("wishlist"),
        related_name="wishes",
    )

    name = models.CharField(
        max_length=150,
        verbose_name=_("name"),
    )

    description = models.TextField(
        verbose_name=_("description"),
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name=_("price"),
    )

    cover = models.ForeignKey(
        "storage.MediaModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("cover"),
        related_name="wish_cover",
    )

    accepted_request = models.ForeignKey(
        "ReservationRequest",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accepted_wish",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
    )
