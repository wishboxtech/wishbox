import json
import uuid

from django.db import transaction
from django.db.models import F, Func, JSONField, Value

from src.apps.profile.models import Avatar


def update_avatar_settings(
    profile_id: str | uuid.UUID, updates: dict[tuple, str]
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
            output_field=JSONField(),
        )

    with transaction.atomic():
        updated = Avatar.objects.filter(profile_id=profile_id).update(settings=expr)
        if updated == 0:
            return 0, None

    settings = Avatar.objects.get(profile_id=profile_id).settings

    return updated, settings
