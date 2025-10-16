import magic
from django.test import TestCase

from src.apps.storage.models import MediaType
from src.utils.fakers import MediaModelFactory


class MediaTypeModelTestCase(TestCase):
    def setUp(self):
        self.media_object = MediaModelFactory()

    def test_create_media_type(self):
        mim_of_media_object = magic.from_buffer(
            self.media_object.file.read(), mime=True
        )
        media_type_object = MediaType.objects.filter(media_type=mim_of_media_object)
        self.assertTrue(media_type_object.exists())
        self.assertEqual(self.media_object.mime_type.id, media_type_object.first().id)
