import hashlib

from django.test import TestCase

from src.utils.fakers import MediaModelFactory


class MediaModelTestCase(TestCase):
    def setUp(self):
        self.media_object = MediaModelFactory()

    def test_media_model_checksum(self):
        sha1_hash = hashlib.sha1()
        content = self.media_object.file.read()
        sha1_hash.update(content)
        digest = sha1_hash.hexdigest()
        self.assertEqual(self.media_object.checksum, digest)
