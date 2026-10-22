"""File transfer and enumeration for the local-to-S3 migration command."""

from src.apps.storage.models import MediaModel


class DjangoMediaCopyRepository:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def names(self):
        yield from MediaModel.objects.exclude(file="").values_list(
            "file", flat=True
        ).distinct().iterator(chunk_size=200)

    def local_exists(self, name):
        return self.source.exists(name)

    def remote_exists(self, name):
        return self.destination.exists(name)

    def copy(self, name):
        with self.source.open(name, "rb") as content:
            saved = self.destination.save(name, content)
        if saved != name:
            self.destination.delete(saved)
            raise RuntimeError(
                "A destination key changed during copying; retry after pausing uploads"
            )
