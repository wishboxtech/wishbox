from django.db import models
from django.utils.translation import gettext_lazy as _


class ReservationRequest(models.Model):
    wish = models.ForeignKey(
        "wishlist.Wish",
        on_delete=models.SET_NULL,
        null=True,
        related_name="reservation_requests",
        verbose_name=_("wish"),
    )

    anonymous_friend = models.ForeignKey(
        "wishlist.AnonymousFriend",
        on_delete=models.SET_NULL,
        null=True,
        related_name="reservation_requests",
        verbose_name=_("anonymous_friend"),
    )

    friend = models.ForeignKey(
        "profile.Profile",
        on_delete=models.SET_NULL,
        null=True,
        related_name="reservation_requests",
        verbose_name=_("friend"),
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )
