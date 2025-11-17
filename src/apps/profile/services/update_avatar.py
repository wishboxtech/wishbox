import json
from typing import Dict

from src.apps.profile.helpers import apply_json_patches, flatten_json
from src.apps.profile.models import AvatarSettings
from src.apps.profile.selectors import get_user_avatar_settings, update_avatar_settings

from src.utils.exceptions import AvatarNotFound, InvalidAvatarSettings


def update_avatar(profile_id, data: Dict) -> Dict:
    """
    Update user avatar based on the provided data
    """
    updated = False

    avatar = get_user_avatar_settings(profile_id=profile_id)
    if not avatar:
        raise AvatarNotFound()

    # Validate Avatar
    flat = flatten_json(data)
    new_data = apply_json_patches(data=avatar.settings, updates=flat)
    try:
        AvatarSettings.model_validate_json(json.dumps(new_data), extra="forbid")
    except Exception:
        raise InvalidAvatarSettings()

    updated, settings = update_avatar_settings(profile_id=profile_id, updates=flat)
    if not updated:
        raise AvatarNotFound()

    return settings
