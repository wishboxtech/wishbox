import uuid
from typing import Union

from django.db.models import F

from src.apps.profile.models import Profile


def get_profile_by_id(profile_id: Union[str, uuid.UUID], lookup: bool = False):
    try:
        if lookup:
            q = Profile.objects.only(
                "profile_id",
                "first_name",
                "last_name",
                "birthdate",
                "gender",
                "photo",
            ).get(profile__id=profile_id)
        else:
            q = (
                Profile.objects.select_related("profile", "photo")
                .annotate(
                    phone_number=F("profile__phone_number"),
                    email=F("profile__email"),
                    is_phone_number_verified=F("profile__is_phone_number_verified"),
                    has_accepted_terms=F("profile__has_accepted_terms"),
                )
                .only(
                    "profile_id",
                    "first_name",
                    "last_name",
                    "birthdate",
                    "gender",
                    "photo",
                    "profile__phone_number",
                    "profile__email",
                    "profile__is_phone_number_verified",
                    "profile__has_accepted_terms",
                )
                .get(profile__id=profile_id)
            )
        return q
    except Profile.DoesNotExist:
        return None
