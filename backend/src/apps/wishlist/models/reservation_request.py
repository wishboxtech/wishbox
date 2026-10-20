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

    guest_identity = models.ForeignKey(
        "wishlist.GuestIdentity",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="gifts",
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("reserved", "Reserved"),
            ("purchased", "Purchased"),
            ("received", "Received"),
            ("cancelled", "Cancelled"),
            ("expired", "Expired"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )

    management_hash = models.CharField(max_length=64, default="", blank=True)

    purchase_by = models.DateField(null=True)
    purchase_plan = models.CharField(max_length=160, default="", blank=True)
    details_checked = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, db_index=True)
    reminder_at = models.DateTimeField(null=True)
    reminded_at = models.DateTimeField(null=True)
    extension_count = models.PositiveSmallIntegerField(default=0)
    received_at = models.DateTimeField(null=True)
    fit = models.CharField(
        max_length=24,
        default="",
        blank=True,
        choices=[
            ("fits", "Fits my wish"),
            ("adjust", "Needs a small change"),
            ("not_for_me", "Not right for me"),
            ("trying", "Still trying it"),
        ],
    )
    private_note = models.TextField(default="", blank=True)
    thank_you = models.TextField(default="", blank=True)
    thank_you_sent_at = models.DateTimeField(null=True)

    follow_up_note = models.TextField(default="", blank=True)
    follow_up_sent_at = models.DateTimeField(null=True)
    follow_up_acknowledged_at = models.DateTimeField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["wish"],
                condition=models.Q(status__in=["reserved", "purchased", "received"]),
                name="one_active_gift_per_wish",
            )
        ]
