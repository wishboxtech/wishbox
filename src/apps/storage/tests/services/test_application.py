import hashlib
from uuid import uuid4

from django.test import TestCase

from src.apps.storage.dto import UploadMediaInputDTO
from src.apps.storage.models import MediaModel
from src.core.composition import storage_service
from src.shared.dto import IdInputDTO


class StorageServiceIntegrationTests(TestCase):
    def test_upload_and_read_plain_dto(self):
        output = storage_service().upload(
            UploadMediaInputDTO(filename="example.txt", content=b"hello")
        )
        media = storage_service().get(IdInputDTO(id=output.media_id))
        self.assertTrue(media.file.endswith(".txt"))
        item = MediaModel.objects.get(id=output.media_id)
        self.assertEqual(item.checksum, hashlib.sha1(b"hello").hexdigest())
        self.assertEqual(item.file.read(), b"hello")

    def test_unknown_media_returns_none(self):
        self.assertIsNone(storage_service().get(IdInputDTO(id=uuid4())))
