from src.apps.storage.selectors import get_media_by_id
from src.apps.storage.serializers import MediaModelSerializer


def serialize_media_by_id(media_id, context=None):
    if context is None:
        context = {}
    media = get_media_by_id(media_id=media_id)
    serializer = MediaModelSerializer(media, context=context)
    serializer_data = serializer.data
    return serializer_data


def serialize_media(media, context=None):
    if context is None:
        context = {}
    serializer = MediaModelSerializer(media, context=context)
    serializer_data = serializer.data
    return serializer_data
