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
        NORMAL_USER = "NU", _("Normal User")
        ADMIN = "AD", _("Admin")

    username = None
    first_name = None
    last_name = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(
        max_length=2,
        choices=UserType.choices,
        default=UserType.NORMAL_USER,
        verbose_name=_("type"),
    )

    email = models.EmailField(
        _("email address"),
        blank=True,
        null=True,
    )

    phone_regex = RegexValidator(
        regex=r"^09\d{9}$",
        message=_("Phone number must be in the format '09#########'."),
    )
    phone_number = models.CharField(
        verbose_name=_("phone number"),
        validators=[phone_regex],
        max_length=11,
        null=True,
        blank=True,
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
    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):

        if not self.email:
            self.email = None
        if not self.phone_number:
            self.phone_number = None

        if not self.password:
            self.set_unusable_password()

        exclude = []
        if self.email is None:
            exclude.append("email")
        if self.phone_number is None:
            exclude.append("phone_number")

        self.full_clean(exclude=exclude)

        if (
            self.email
            and User.objects.exclude(pk=self.pk).filter(email=self.email).exists()
        ):
            raise ValueError(f"User with email {self.email} already exists.")
        if (
            self.phone_number
            and User.objects.exclude(pk=self.pk)
            .filter(phone_number=self.phone_number)
            .exists()
        ):
            raise ValueError(f"User with phone {self.phone_number} already exists.")

        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
