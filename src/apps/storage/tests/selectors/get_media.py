from django.test import TestCase

from src.apps.storage.selectors import get_media_by_id
from src.utils.fakers import MediaModelFactory


class GetMediaSelectorTestCase(TestCase):
    def setUp(self):
        self.media = MediaModelFactory()

    def tests_get_media_by_id_selector(self):
        media = get_media_by_id(self.media.id)
        self.assertEqual(media, self.media)
