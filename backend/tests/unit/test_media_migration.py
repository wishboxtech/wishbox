from unittest import TestCase
from unittest.mock import Mock

from src.apps.storage.interfaces import MediaCopyRepository
from src.apps.storage.services.migration import MediaMigrationService


class MediaMigrationTests(TestCase):
    def test_dry_run_reports_missing_and_existing_without_writing(self):
        repository = Mock(spec=MediaCopyRepository)
        repository.names.return_value = ("existing.txt", "new.txt", "missing.txt")
        repository.remote_exists.side_effect = lambda name: name == "existing.txt"
        repository.local_exists.side_effect = lambda name: name == "new.txt"
        result = MediaMigrationService(repository).copy()
        self.assertEqual(
            (result.existing, result.would_copy, result.missing, result.copied),
            (1, 1, 1, 0),
        )
        repository.copy.assert_not_called()

    def test_only_missing_remote_files_are_copied(self):
        repository = Mock(spec=MediaCopyRepository)
        repository.names.return_value = ("existing.txt", "new.txt")
        repository.remote_exists.side_effect = lambda name: name == "existing.txt"
        repository.local_exists.return_value = True
        result = MediaMigrationService(repository).copy(dry_run=False)
        repository.copy.assert_called_once_with("new.txt")
        self.assertEqual((result.copied, result.existing), (1, 1))
