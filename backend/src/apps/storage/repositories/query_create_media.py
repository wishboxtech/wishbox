from django.db import transaction

from src.apps.storage.models import MediaModel


@transaction.atomic
def create_media(media):
    media_object = MediaModel.objects.create(file=media)
    return media_object
