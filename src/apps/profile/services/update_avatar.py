import copy
import json
from typing import Dict

from src.apps.profile.models import AvatarSettings
from src.apps.profile.helpers import apply_json_patches, flatten_json
from src.apps.profile.selectors import get_user_avatar_settings, update_avatar_settings
from src.apps.profile.serializers import EditeAvatarSerializer
from src.static import SerializerErrors

from src.utils.exceptions import InvalidAvatarSettings, AvatarNotFound


def update_avatar(profile_id, data: Dict) -> int:
    """
    Update user avatar based on the provided data
    """
    errs = {}
    updated = False
    avatar_data = None

    avatar = get_user_avatar_settings(profile_id=profile_id)
    if not avatar.settings:
        raise AvatarNotFound()

    # Validate Avatar
    flat = flatten_json(data)
    new_data = apply_json_patches(data=avatar.settings, updates=flat)
    try:
        AvatarSettings.model_validate_json(json.dumps(new_data), extra="forbid")
    except Exception:
        raise InvalidAvatarSettings()

    updated = update_avatar_settings(profile_id=profile_id, updates=flat)
    return updated
