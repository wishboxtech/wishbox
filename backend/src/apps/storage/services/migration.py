"""Copy existing uploads without changing database keys or removing local files."""

from src.apps.storage.dto import CopyMediaOutputDTO
from src.apps.storage.interfaces import MediaCopyRepository


class MediaMigrationService:
    def __init__(self, repository: MediaCopyRepository):
        self.repository = repository

    def copy(self, dry_run: bool = True) -> CopyMediaOutputDTO:
        copied = would_copy = existing = missing = 0
        for name in self.repository.names():
            if self.repository.remote_exists(name):
                existing += 1
            elif not self.repository.local_exists(name):
                missing += 1
            elif dry_run:
                would_copy += 1
            else:
                self.repository.copy(name)
                copied += 1
        return CopyMediaOutputDTO(
            copied=copied, would_copy=would_copy, existing=existing, missing=missing
        )
