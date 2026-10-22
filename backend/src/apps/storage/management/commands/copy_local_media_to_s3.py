"""An explicit, repeatable migration for existing local uploads."""

from django.core.management.base import BaseCommand, CommandError

from src.core.composition import media_migration_service


class Command(BaseCommand):
    help = (
        "Copy database-referenced local uploads to configured S3, preserving file keys"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true", help="Check files without uploading"
        )

    def handle(self, *args, **options):
        try:
            result = media_migration_service().copy(dry_run=options["dry_run"])
        except ValueError as error:
            raise CommandError(str(error)) from error
        self.stdout.write(result.model_dump_json())
        if result.missing:
            raise CommandError(
                f"{result.missing} referenced files are missing both locally and on S3"
            )
