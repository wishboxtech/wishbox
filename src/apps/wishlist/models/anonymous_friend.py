import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


# may need to collect peoples IP for further restrictions
# may need to use another Database for this anonymous users, it works fine for now
class AnonymousFriend(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nickname = models.CharField(
        max_length=150,
        verbose_name=_("nickname"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
    )
