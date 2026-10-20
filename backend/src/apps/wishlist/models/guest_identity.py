from django.db import models


class GuestIdentity(models.Model):
    """One browser secret; only its digest is persisted."""

    key_hash = models.CharField(max_length=64, unique=True)
    claimed_user = models.OneToOneField(
        "authentication.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="claimed_guest_identity",
    )
    consumed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
