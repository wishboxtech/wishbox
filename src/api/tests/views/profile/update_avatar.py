from django.test import LiveServerTestCase
from django.urls import reverse
from rest_framework.test import RequestsClient

from src.core.composition import authentication_service
from src.shared.dto import IdInputDTO
from src.utils.fakers import AvatarFactory, AvatarWidgetsFactory, ProfileFactory


class UpdateAvatarTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()

        self.profile = ProfileFactory()
        self.avatar = AvatarFactory(profile=self.profile)
        self.avatar_widget = AvatarWidgetsFactory(type="Face")
        self.access_token_with_profile = (
            authentication_service()
            .login(IdInputDTO(id=self.profile.profile_id))
            .model_dump()
            .get("access_token")
        )

    def make_request(self, headers=None, data=None):
        url = self.live_server_url + reverse("avatar")
        return self.rc.patch(url, headers=headers, json=data)

    def test_unauthorized(self):
        response = self.make_request()
        self.assertEqual(response.status_code, 401)

    def test_valid_update_avatar(self):
        widgets = self.avatar.settings.get("widgets")
        face = widgets.get("face")
        self.assertNotEqual(face.get("shape"), str(self.avatar_widget.id))
        update_data = {
            "widgets": {
                "face": {"shape": str(self.avatar_widget.id)},
            }
        }
        response = self.make_request(
            headers={"access": self.access_token_with_profile}, data=update_data
        )
        data = response.json().get("data")
        updated_widgets = data.get("widgets")
        updated_face = updated_widgets.get("face")
        self.assertEqual(updated_face.get("shape"), str(self.avatar_widget.id))
        self.assertEqual(response.status_code, 200)

    def test_invalid_update_avatar(self):
        invalid_data = {
            "widgets": {
                "body": "invalud",
            }
        }
        response = self.make_request(
            headers={"access": self.access_token_with_profile}, data=invalid_data
        )
        self.assertEqual(response.status_code, 400)
