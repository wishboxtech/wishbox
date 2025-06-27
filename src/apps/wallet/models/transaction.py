import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        Transfer = "TR", _("Transfer")
        Receive = "RC", _("Receive")
        Payment = "PY", _("Payment")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card = models.ForeignKey(
        "wallet.Card",
        models.CASCADE,
        related_name="transactions",
        verbose_name=_("card"),
    )
    type = models.CharField(
        max_length=2,
        choices=TransactionType.choices,
        default=TransactionType.Payment,
        verbose_name=_("type"),
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )
