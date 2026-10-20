from django.test import LiveServerTestCase
from django.urls import reverse
from rest_framework.test import RequestsClient

from src.core.composition import authentication_service
from src.shared.dto import IdInputDTO
from src.utils.fakers import ProfileFactory, UserFactory, WishlistFactory


class GetWishlistsAPIViewTestCase(LiveServerTestCase):
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
        self.wishlists = WishlistFactory.create_batch(5, profile=self.profile)

        self.solid_user = UserFactory()
        self.access_token = (
            authentication_service()
            .login(IdInputDTO(id=self.solid_user.id))
            .model_dump()
            .get("access_token")
        )

    def make_request(self, headers=None):
        url = self.live_server_url + reverse("wishlist")
        return self.rc.get(url, headers=headers)

    def test_unauthorized(self):
        response = self.make_request()
        self.assertEqual(response.status_code, 401)

    def test_ok_response(self):
        response = self.make_request(headers={"access": self.access_token_with_profile})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("ok"), True)
        data = response.json().get("data")
        self.assertEqual(len(data), 5)
