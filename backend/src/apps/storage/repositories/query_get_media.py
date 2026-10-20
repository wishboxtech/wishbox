import uuid

from src.apps.storage.models import MediaModel


def get_media_by_id(media_id: str | uuid.UUID):
    media = MediaModel.objects.get(id=media_id)
    return media
