from django.test import LiveServerTestCase
from django.urls import reverse
from faker import Faker
from rest_framework.test import RequestsClient

from src.core.composition import authentication_service
from src.shared.dto import IdInputDTO
from src.static import SerializerErrors
from src.utils.fakers import ProfileFactory, UserFactory


class CreateUpdateProfileTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()

        self.user_with_profile = UserFactory()
        self.profile = ProfileFactory(profile_id=self.user_with_profile.id)
        self.access_token_with_profile = (
            authentication_service()
            .login(IdInputDTO(id=self.user_with_profile.id))
            .model_dump()
            .get("access_token")
        )

        self.solid_user = UserFactory()
        self.access_token = (
            authentication_service()
            .login(IdInputDTO(id=self.solid_user.id))
            .model_dump()
            .get("access_token")
        )

    def make_request(self, headers=None, data=None):
        url = self.live_server_url + reverse("profile")
        return self.rc.put(url, headers=headers, json=data)

    def test_unauthorized(self):
        response = self.make_request()
        self.assertEqual(response.status_code, 401)

    def test_valid_create_profile(self):
        data = {"first_name": Faker().first_name(), "last_name": Faker().last_name()}
        response = self.make_request(headers={"access": self.access_token}, data=data)
        self.assertEqual(response.status_code, 202)
        result = response.json().get("data")
        self.assertEqual(result.get("first_name"), data["first_name"])
        self.assertEqual(result.get("last_name"), data["last_name"])
        self.assertEqual(response.json().get("created"), True)

    def test_valid_update_profile(self):
        data = {
            "first_name": f"{self.profile.first_name} updated",
            "last_name": f"{self.profile.last_name} updated",
        }

        self.assertNotEqual(self.profile.first_name, data["first_name"])
        self.assertNotEqual(self.profile.last_name, data["last_name"])
        response = self.make_request(
            headers={"access": self.access_token_with_profile}, data=data
        )
        self.assertEqual(response.status_code, 202)
        result = response.json().get("data")
        self.assertEqual(result.get("first_name"), data["first_name"])
        self.assertEqual(result.get("last_name"), data["last_name"])
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, data["first_name"])
        self.assertEqual(self.profile.last_name, data["last_name"])
        self.assertEqual(response.json().get("created"), False)

    def test_invalid_create_profile(self):
        data = {
            "first_name": Faker().first_name(),
            "last_name": Faker().last_name(),
            "gender": "M",  # should be 'male' to work
        }
        response = self.make_request(
            headers={"access": self.access_token_with_profile}, data=data
        )
        self.assertEqual(response.status_code, 400)
        error_types = response.json().get("error_type")
        self.assertEqual(
            error_types[0], SerializerErrors.CreateProfile.errors.get("gender")
        )
