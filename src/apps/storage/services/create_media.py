from src.apps.storage.selectors import create_media as create_media_selector


def create_media(media):
    media_object = create_media_selector(media=media)
    return media_object.id
