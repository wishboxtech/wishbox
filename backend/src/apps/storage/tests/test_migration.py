from io import StringIO
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from src.apps.storage.models import MediaModel
from src.apps.storage.repositories.migration import DjangoMediaCopyRepository
from src.apps.storage.services.migration import MediaMigrationService


class MediaCopyTests(TestCase):
    def test_keys_and_contents_are_preserved_and_copy_is_repeatable(self):
        with TemporaryDirectory() as source_dir, TemporaryDirectory() as target_dir:
            source = FileSystemStorage(location=source_dir)
            target = FileSystemStorage(location=target_dir)
            name = source.save(
                "text/plain/original.txt", ContentFile(b"existing photo bytes")
            )
            MediaModel.objects.bulk_create(
                [MediaModel(file=name), MediaModel(file=name)]
            )
            service = MediaMigrationService(DjangoMediaCopyRepository(source, target))
            dry_run = service.copy(dry_run=True)
            self.assertEqual(dry_run.would_copy, 1)
            self.assertFalse(target.exists(name))
            self.assertEqual(service.copy(dry_run=False).copied, 1)
            self.assertTrue(source.exists(name))
            with target.open(name) as copied:
                self.assertEqual(copied.read(), b"existing photo bytes")
            self.assertEqual(service.copy(dry_run=False).existing, 1)
            self.assertEqual(
                set(MediaModel.objects.values_list("file", flat=True)), {name}
            )

    def test_command_requires_s3_and_reports_missing_files(self):
        with self.assertRaisesMessage(CommandError, "Enable USE_S3"):
            call_command("copy_local_media_to_s3", dry_run=True)
        with TemporaryDirectory() as source_dir, TemporaryDirectory() as target_dir:
            MediaModel.objects.bulk_create([MediaModel(file="missing.txt")])
            service = MediaMigrationService(
                DjangoMediaCopyRepository(
                    FileSystemStorage(location=source_dir),
                    FileSystemStorage(location=target_dir),
                )
            )
            with patch(
                "src.apps.storage.management.commands.copy_local_media_to_s3.media_migration_service",
                return_value=service,
            ), self.assertRaisesMessage(CommandError, "missing both locally and on S3"):
                output = StringIO()
                call_command("copy_local_media_to_s3", dry_run=True, stdout=output)
            self.assertIn('"missing":1', output.getvalue())
