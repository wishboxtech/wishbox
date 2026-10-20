from uuid import uuid4

from django.test import TestCase

from src.apps.profile.domain.errors import AvatarNotFound, InvalidAvatarSettings
from src.apps.profile.dto import UpdateAvatarInputDTO, UpsertProfileInputDTO
from src.core.composition import profile_service
from src.shared.dto import IdInputDTO
from src.utils.fakers import AvatarFactory, UserFactory


class ProfileServiceIntegrationTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.service = profile_service()

    def test_create_and_update_profile_keeps_identity(self):
        output = self.service.upsert_profile(
            UpsertProfileInputDTO(profile_id=self.user.id, first_name="Sara")
        )
        self.assertTrue(output.created)
        updated = self.service.upsert_profile(
            UpsertProfileInputDTO(profile_id=self.user.id, last_name="Ahmadi")
        )
        self.assertFalse(updated.created)
        self.assertEqual(updated.profile.first_name, "Sara")
        self.assertEqual(updated.profile.phone_number, self.user.phone_number)
        self.assertTrue(self.service.exists(self.user.id))

    def test_missing_profile_and_avatar_return_none(self):
        self.assertIsNone(self.service.get_profile(IdInputDTO(id=uuid4())))
        self.assertIsNone(self.service.get_avatar(IdInputDTO(id=uuid4())))

    def test_avatar_patch_is_validated_and_persisted(self):
        avatar = AvatarFactory()
        output = self.service.update_avatar(
            UpdateAvatarInputDTO(
                profile_id=avatar.profile_id, changes={"background": {"color": "red"}}
            )
        )
        self.assertEqual(output.settings.background.color, "red")
        avatar.refresh_from_db()
        self.assertEqual(avatar.settings["background"]["color"], "red")

    def test_invalid_avatar_patch_does_not_change_data(self):
        avatar = AvatarFactory()
        before = avatar.settings
        with self.assertRaises(InvalidAvatarSettings):
            self.service.update_avatar(
                UpdateAvatarInputDTO(
                    profile_id=avatar.profile_id, changes={"gender": 123}
                )
            )
        avatar.refresh_from_db()
        self.assertEqual(avatar.settings, before)

    def test_missing_avatar_write_raises_domain_error(self):
        with self.assertRaises(AvatarNotFound):
            self.service.update_avatar(
                UpdateAvatarInputDTO(profile_id=uuid4(), changes={"gender": "male"})
            )
