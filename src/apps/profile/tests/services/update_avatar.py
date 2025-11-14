import faker
from django.test import TestCase


from src.apps.profile.services import update_avatar
from src.utils.fakers import AvatarFactory, ProfileFactory


class UpdateAvatarTestCase(TestCase):
    def setUp(self):
        self.profile = ProfileFactory()
        self.avatar = AvatarFactory(profile=self.profile)

    def test_update_avatar(self):
        update_avatar(
            profile_id=self.profile.profile_id,
            data={
                "gender": "KIIIIR",
                "widgets": {
                    "face": {"shape": "round"},
                    "eyes": {"shape": "kiri"},
                },
            },
        )
