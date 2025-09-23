from src.apps.storage.serializers import MediaModelSerializer


def serialize_batch_of_media(media, context=None):
    if context is None:
        context = {}
    serializer = MediaModelSerializer(media, context=context, many=True)
    serializer_data = serializer.data
    return serializer_data
