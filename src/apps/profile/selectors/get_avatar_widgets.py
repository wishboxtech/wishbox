from src.apps.profile.models import AvatarWidgets


def get_avatar_widgets():
    return (
        AvatarWidgets.objects.only(
            "id",
            "type",
            "is_premium",
            "is_active",
            "image",
        )
        .order_by("type")
        .all()
    )
