from contextlib import nullcontext
from datetime import datetime, timezone
from unittest import TestCase
from unittest.mock import Mock
from uuid import uuid4

from src.apps.storage.domain import Media
from src.apps.storage.dto import UploadMediaInputDTO
from src.apps.storage.interfaces import MediaRepository
from src.apps.storage.services import StorageService
from src.apps.website.domain import Contact
from src.apps.website.dto import ListContactsInputDTO
from src.apps.website.interfaces import ContactRepository
from src.apps.website.services import WebsiteService
from src.shared.domain.errors import NotFound


class StorageWebsiteUnitTests(TestCase):
    def test_upload_accepts_plain_bytes_and_returns_id(self):
        repo = Mock(spec=MediaRepository)
        id = uuid4()
        repo.create.return_value = Media(id, "/file.txt")
        dto = UploadMediaInputDTO(filename="file.txt", content=b"hello")
        result = StorageService(repo, nullcontext).upload(dto)
        self.assertEqual(result.media_id, id)
        repo.create.assert_called_once_with(dto)

    def test_media_batch_preserves_identity(self):
        repo = Mock(spec=MediaRepository)
        media = Media(uuid4(), "/image.png")
        repo.get_many.return_value = (media,)
        result = StorageService(repo, nullcontext).get_media_batch((media.id,))
        self.assertEqual(result[media.id].file, "/image.png")

    def test_contacts_return_typed_output(self):
        repo = Mock(spec=ContactRepository)
        now = datetime.now(timezone.utc)
        repo.list.return_value = (Contact(uuid4(), "a@example.com", now, now),)
        self.assertEqual(
            WebsiteService(repo).list_contacts(ListContactsInputDTO())[0].email,
            "a@example.com",
        )

    def test_empty_contacts_raise_domain_error(self):
        repo = Mock(spec=ContactRepository)
        repo.list.return_value = ()
        with self.assertRaises(NotFound):
            WebsiteService(repo).list_contacts(ListContactsInputDTO())
