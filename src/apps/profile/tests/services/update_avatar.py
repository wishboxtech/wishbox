from django.test import TestCase

from src.apps.profile.models import Avatar
from src.apps.profile.services import update_avatar
from src.utils.exceptions import AvatarNotFound, InvalidAvatarSettings
from src.utils.fakers import AvatarFactory, ProfileFactory


class UpdateAvatarTestCase(TestCase):
    def setUp(self):
        self.profile = ProfileFactory()
        self.avatar = AvatarFactory(profile=self.profile)

    def test_update_avatar(self):
        old_gender = self.avatar.settings.get("gender")

        settings = update_avatar(
            profile_id=self.profile.profile_id,
            data={
                "gender": "RANDOM_GENDER",
                "widgets": {
                    "face": {"shape": "round"},
                    "eyes": {"shape": "original"},
                },
            },
        )

        self.assertEqual(settings.get("gender"), "RANDOM_GENDER")
        self.assertNotEqual(settings.get("gender"), old_gender)
        self.assertEqual(settings["widgets"]["face"]["shape"], "round")
        self.assertEqual(settings["widgets"]["eyes"]["shape"], "original")

        # Ensure DB is updated
        self.avatar.refresh_from_db()
        self.assertEqual(self.avatar.settings["gender"], "RANDOM_GENDER")

    def test_invalid_settings_raises(self):
        """
        Provide a field that definitely breaks AvatarSettings validation.
        For example: sending a type that violates pydantic model schema.
        """
        with self.assertRaises(InvalidAvatarSettings):
            update_avatar(
                profile_id=self.profile.profile_id,
                data={
                    "gender": 99999,
                },
            )

    def test_update_returns_zero_rows(self):
        """
        Delete avatar before calling update so the update query affects 0 rows.
        """
        self.avatar.delete()

        with self.assertRaises(AvatarNotFound):
            update_avatar(
                profile_id=self.profile.profile_id,
                data={"gender": "NEW_GENDER"},
            )
