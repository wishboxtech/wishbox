from django.test import TestCase

from src.apps.storage.serializers import MediaModelSerializer
from src.apps.storage.services import serialize_batch_of_media
from src.utils.fakers import MediaModelFactory


class SerializeBatchOfMediaServiceTestCase(TestCase):
    def setUp(self):
        self.media = MediaModelFactory.create_batch(4)

    def test_serialize_batch_of_media_serivce(self):
        serialized_by_service = serialize_batch_of_media(self.media)
        serialized_by_serializer = MediaModelSerializer(
            self.media, many=True
        ).data
        self.assertEqual(serialized_by_serializer, serialized_by_service)
