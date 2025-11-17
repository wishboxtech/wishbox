from django.core.exceptions import ValidationError
from django.test import TestCase

from src.utils.fakers import AvatarFactory, ProfileFactory


class AvatarModelTestCase(TestCase):
    def setUp(self):
        self.profile = ProfileFactory()
        self.avatar = AvatarFactory(profile=self.profile)

    def test_clean_method_avatar(self):
        # test gender
        with self.assertRaises(ValidationError):
            AvatarFactory(settings={"gender": "M"})
