import uuid
from typing import Union

from src.apps.profile.models import Profile

def get_profile_by_id(profile_id: Union[str, uuid.UUID]):
    try:
        return Profile.objects.get(profile__id=profile_id)
    except Profile.DoesNotExist:
        return None