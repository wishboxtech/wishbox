import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.apps.authentication.models.user_manager import UserManager


REQUIRED_FIELDS_FOR_EACH_USER = {
    "NU": [
        "phone_number",
    ],
    "AD": [],
}


class User(AbstractUser):
    class UserType(models.TextChoices):
        FOOTBALLIHA_USER = "NU", _("Normal User")
        ADMIN = "AD", _("Admin")

    username = None
    first_name = None
    last_name = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(
        max_length=2,
        choices=UserType.choices,
        default=UserType.FOOTBALLIHA_USER,
        verbose_name=_("type"),
    )

    phone_regex = RegexValidator(
        regex=r"^09\d{9}$",
        message=_("Phone number must be in the format '09#########'."),
    )
    phone_number = models.CharField(
        verbose_name=_("phone number"),
        validators=[phone_regex],
        max_length=11,
        unique=True,
    )
    
    has_accepted_terms = models.BooleanField(
        default=False,
        verbose_name=_("has accepted terms"),
    )

    is_phone_number_verified = models.BooleanField(
        default=False,
        verbose_name=_("is phone number verified"),
    )
    phone_number_verified_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("phone number verified at"),
    )
    objects = UserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.password is None or self.password == "":
            self.set_unusable_password()
        self.full_clean()
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
