import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="wallets",
        verbose_name=_("user"),
    )
    card_number_regex = RegexValidator(
        regex=r"^[0-9]{16}$",
        message=_("Card number must be 16 digits long."),
    )
    card_number = models.CharField(
        verbose_name=_("card number"),
        validators=[card_number_regex],
        max_length=16,
        unique=True,
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name=_("is approved"),
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )
