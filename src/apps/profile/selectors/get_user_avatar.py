import uuid
from typing import Union

from src.apps.profile.models import Avatar


def get_user_avatar_settings(profile_id: Union[str, uuid.UUID]):
    try:
        return Avatar.objects.only("settings").get(
            profile_id=profile_id,
        )
    except Avatar.DoesNotExist:
        return None
