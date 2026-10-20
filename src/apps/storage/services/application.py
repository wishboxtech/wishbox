from uuid import UUID

from src.apps.storage.dto import (
    MediaOutputDTO,
    UploadMediaInputDTO,
    UploadMediaOutputDTO,
)
from src.apps.storage.interfaces import MediaRepository
from src.shared.dto import IdInputDTO
from src.shared.interfaces import TransactionBoundary


class StorageService:
    def __init__(self, repository: MediaRepository, transaction: TransactionBoundary):
        self.repository = repository
        self.transaction = transaction

    def upload(self, dto: UploadMediaInputDTO) -> UploadMediaOutputDTO:
        with self.transaction():
            media = self.repository.create(dto)
        return UploadMediaOutputDTO(media_id=media.id)

    def get(self, dto: IdInputDTO) -> MediaOutputDTO | None:
        return self.get_media(dto.id)

    def get_media(self, id: UUID) -> MediaOutputDTO | None:
        media = self.repository.get(id)
        return MediaOutputDTO(file=media.file) if media else None

    def get_media_batch(self, ids: tuple[UUID, ...]) -> dict[UUID, MediaOutputDTO]:
        return {
            media.id: MediaOutputDTO(file=media.file)
            for media in self.repository.get_many(ids)
        }
