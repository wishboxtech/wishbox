from django.test import LiveServerTestCase, tag
from django.urls import reverse
from faker import Faker
from rest_framework.test import RequestsClient

from src.utils.fakers import (
    ProfileFactory,
    UserFactory,
    WishFactory,
    WishlistFactory,
    AnonymousFriendFactory,
)


class SubmitRequestAPIViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()

        self.user1 = UserFactory()
        self.profile1 = ProfileFactory(profile_id=self.user1.id)
        self.wishlist = WishlistFactory(profile=self.profile1)

        self.user2 = UserFactory()
        self.profile2 = ProfileFactory(profile_id=self.user2.id)

        self.anonymous_friend = AnonymousFriendFactory()

        self.wishes = WishFactory.create_batch(3, wishlist=self.wishlist)

    def test_valid_submit_request_friend_api(self):
        url = self.live_server_url + reverse(
            "submit_request", kwargs={"id": str(self.wishes[0].id)}
        )
        body = {"friend": str(self.profile2.pk)}
        response = self.rc.post(url, json=body)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json().get("data").get("wish"), str(self.wishes[0].id)
        )
        self.assertEqual(
            response.json().get("data").get("friend"), str(self.profile2.pk)
        )
        self.assertEqual(response.json().get("created"), True)

    def test_valid_submit_anonymous_friend_api(self):
        url = self.live_server_url + reverse(
            "submit_request", kwargs={"id": str(self.wishes[1].id)}
        )
        body = {"anonymous_friend": str(self.anonymous_friend.pk)}
        response = self.rc.post(url, json=body)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json().get("data").get("wish"), str(self.wishes[1].id)
        )
        self.assertEqual(
            response.json().get("data").get("anonymous_friend"),
            str(self.anonymous_friend.pk),
        )
        self.assertEqual(response.json().get("created"), True)

    def test_invalid_submit_request_empty_body_api(self):
        url = self.live_server_url + reverse(
            "submit_request", kwargs={"id": str(self.wishes[1].id)}
        )
        response = self.rc.post(url)

        self.assertEqual(response.status_code, 400)