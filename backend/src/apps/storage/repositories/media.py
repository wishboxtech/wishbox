from django.core.files.base import ContentFile

from src.apps.storage.domain import Media
from src.apps.storage.models import MediaModel


def media_entity(instance):
    return Media(id=instance.id, file=instance.file.url if instance.file else "")


class DjangoMediaRepository:
    def get_many(self, ids):
        return tuple(
            media_entity(item)
            for item in MediaModel.objects.filter(id__in=ids).only("id", "file")
        )

    def get(self, id):
        instance = MediaModel.objects.filter(id=id).first()
        return media_entity(instance) if instance else None

    def create(self, dto):
        instance = MediaModel.objects.create(
            file=ContentFile(dto.content, name=dto.filename)
        )
        return media_entity(instance)
