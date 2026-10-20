from contextlib import nullcontext
from unittest import TestCase
from unittest.mock import Mock
from uuid import UUID, uuid4

from src.apps.profile.domain.avatar import AvatarSettings
from src.apps.profile.domain.errors import InvalidAvatarSettings
from src.apps.profile.dto import UpdateAvatarInputDTO
from src.apps.profile.interfaces import ProfileRepository, AuthenticationServiceProtocol
from src.apps.profile.services import ProfileService
from src.apps.storage.dto import MediaOutputDTO
from src.apps.storage.interfaces import StorageServiceProtocol
from src.shared.dto import IdInputDTO


def avatar_settings():
    return AvatarSettings(
        wrapper_shape="circle",
        background={"color": "white", "border_color": "black"},
        gender="male",
        widgets={
            name: {"shape": str(uuid4()), "fill_color": "blue"}
            for name in (
                "ear",
                "face",
                "tops",
                "eyes",
                "nose",
                "mouth",
                "beard",
                "clothes",
                "glasses",
                "earrings",
                "eyebrows",
            )
        },
    )


class ProfileUnitTests(TestCase):
    def setUp(self):
        self.repo = Mock(spec=ProfileRepository)
        self.storage = Mock(spec=StorageServiceProtocol)
        self.service = ProfileService(
            self.repo,
            Mock(spec=AuthenticationServiceProtocol),
            self.storage,
            nullcontext,
        )
        self.id = uuid4()
        self.settings = avatar_settings()
        self.repo.get_avatar.return_value = self.settings

    def test_patch_preserves_unmentioned_settings(self):
        output = self.service.update_avatar(
            UpdateAvatarInputDTO(
                profile_id=self.id, changes={"background": {"color": "red"}}
            )
        )
        self.assertEqual(output.settings.background.color, "red")
        self.assertEqual(output.settings.background.border_color, "black")
        self.assertEqual(self.settings.background.color, "white")
        self.repo.get_avatar.assert_called_once_with(self.id, lock=True)

    def test_invalid_nested_field_is_rejected_without_saving(self):
        for changes in (
            {"widgets": {"face": {"unknown": "value"}}},
            {"background": {"unknown": {}}},
            {"gender": 5},
        ):
            with self.subTest(changes=changes), self.assertRaises(
                InvalidAvatarSettings
            ):
                self.service.update_avatar(
                    UpdateAvatarInputDTO(profile_id=self.id, changes=changes)
                )
        self.repo.save_avatar.assert_not_called()

    def test_missing_widget_does_not_shift_another_widgets_image(self):
        eyes = self.settings.widgets.eyes.shape
        media_id = uuid4()
        self.repo.widget_media_ids.return_value = {UUID(eyes): media_id}
        self.storage.get_media_batch.return_value = {
            media_id: MediaOutputDTO(file="/eyes.png")
        }
        output = self.service.get_avatar(IdInputDTO(id=self.id))
        self.assertIsNone(output.widgets["face"].image)
        self.assertEqual(output.widgets["eyes"].image.file, "/eyes.png")
        self.assertEqual(self.settings.widgets.eyes.shape, eyes)

    def test_duplicate_shapes_share_the_same_image(self):
        data = self.settings.model_dump()
        data["widgets"]["face"]["shape"] = data["widgets"]["eyes"]["shape"]
        self.repo.get_avatar.return_value = AvatarSettings.model_validate(data)
        media_id = uuid4()
        self.repo.widget_media_ids.return_value = {
            UUID(data["widgets"]["eyes"]["shape"]): media_id
        }
        self.storage.get_media_batch.return_value = {
            media_id: MediaOutputDTO(file="/shared.png")
        }
        output = self.service.get_avatar(IdInputDTO(id=self.id))
        self.assertEqual(output.widgets["face"].image, output.widgets["eyes"].image)
