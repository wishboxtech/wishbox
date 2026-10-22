from typing import Protocol
from collections.abc import Iterable
from uuid import UUID

from src.apps.storage.domain import Media
from src.apps.storage.dto import MediaOutputDTO, UploadMediaInputDTO


class MediaRepository(Protocol):
    def get(self, id: UUID) -> Media | None:
        ...

    def get_many(self, ids: tuple[UUID, ...]) -> tuple[Media, ...]:
        ...

    def create(self, dto: UploadMediaInputDTO) -> Media:
        ...


class StorageServiceProtocol(Protocol):
    """StorageService capabilities required by profile and wishlist services."""

    def get_media(self, id: UUID) -> MediaOutputDTO | None:
        ...

    def get_media_batch(self, ids: tuple[UUID, ...]) -> dict[UUID, MediaOutputDTO]:
        ...


class MediaCopyRepository(Protocol):
    def names(self) -> Iterable[str]:
        ...

    def local_exists(self, name: str) -> bool:
        ...

    def remote_exists(self, name: str) -> bool:
        ...

    def copy(self, name: str) -> None:
        ...
