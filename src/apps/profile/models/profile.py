import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Profile(models.Model):
    profile = models.OneToOneField(
        "authentication.User",
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_("id"),
    )

    first_name = models.CharField(
        max_length=150,
        verbose_name=_("first name"),
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=150,
        verbose_name=_("last name"),
        blank=True,
        null=True,
    )

    birthdate = models.DateField(
        verbose_name=_("birthdate"),
        blank=True,
        null=True,
    )

    bio = models.CharField(
        max_length=250,
        verbose_name=_("bio"),
        blank=True,
        null=True
    )

    class Gender(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        verbose_name=_("gender"),
        blank=True,
        null=True,
    )

    photo = models.ForeignKey(
        "storage.MediaModel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("photo"),
        related_name="profile_photo",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
    )