import uuid
from typing import Union

from django.db.models import Case, When

from src.apps.profile.models import AvatarWidgets


def get_avatar_widgets():
    return (
        AvatarWidgets.objects.prefetch_related("colors")
        .only(
            "id",
            "type",
            "is_premium",
            "colors",
            "is_active",
            "image",
        )
        .order_by("type")
        .all()
    )


def get_avatar_widget_images_by_id(ids: list[Union[str, uuid.UUID]]):
    order = Case(*[When(id=id, then=pos) for pos, id in enumerate(ids)])
    return AvatarWidgets.objects.filter(id__in=ids).order_by(order).only("image")
