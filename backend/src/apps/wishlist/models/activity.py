import uuid

from django.db import models


class WishInteraction(models.Model):
    wish = models.ForeignKey(
        "wishlist.Wish", on_delete=models.CASCADE, related_name="interactions"
    )
    visitor = models.CharField(max_length=80)
    viewed = models.BooleanField(default=False)
    liked = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["wish", "visitor"], name="unique_wish_visitor"
            )
        ]


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(
        "profile.Profile", on_delete=models.CASCADE, related_name="wish_notifications"
    )
    wish = models.ForeignKey("wishlist.Wish", null=True, on_delete=models.SET_NULL)
    wish_name = models.CharField(max_length=150)
    event = models.CharField(max_length=20)
    read_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["profile", "-created_at"], name="notification_inbox_idx"
            )
        ]
