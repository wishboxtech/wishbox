from src.apps.profile.selectors import (
    get_avatar_widget_images_by_id,
    get_user_avatar_settings,
)
from src.apps.storage.services import serialize_media


def get_user_avatar(profile_id) -> dict | None:
    """
    Return serialized avatar data for a given profile_id.
    Returns None if Avatar does not exists
    """
    user_avatar = get_user_avatar_settings(profile_id=profile_id)
    if not user_avatar:
        return None

    settings = user_avatar.settings
    widgets: dict = settings.get("widgets")

    ids = [v.get("shape") for v in widgets.values()]

    # in this selector order fixed with a order function, check the code...
    widget_images = get_avatar_widget_images_by_id(ids)

    # This should logs when PHOTOS not equal
    if widget_images.count() != len(ids):
        ...

    # now add image and remove shape id for a clean response
    # we dont have any serializer because the setting is already a json
    for i, widget in enumerate(widgets.values()):
        try:
            widget["image"] = serialize_media(widget_images[i].image)
        except IndexError as e:
            # should logs Index error
            # this error happens when we have widget inside the settings but its not in DB
            widget["image"] = None
    settings["widgets"] = widgets

    return settings
