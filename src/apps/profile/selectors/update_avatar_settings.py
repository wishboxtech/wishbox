import json
import uuid
from typing import Dict, Tuple, Union

from django.db.models import F, Func, Value

from src.apps.profile.models import Avatar


def update_avatar_settings(
    profile_id: Union[str, uuid.UUID], updates: Dict[Tuple, str]
) -> int:
    """
    Partially update a key inside Avatar.settings JSONField.
    """
    expr = F("settings")
    for path, value in updates.items():
        expr = Func(
            expr,
            Value("{" + ",".join(path) + "}"),
            Value(json.dumps(value)),
            function="jsonb_set",
        )

    return Avatar.objects.filter(profile_id=profile_id).update(settings=expr)
