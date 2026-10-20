from datetime import date, timedelta

from django.urls import reverse
from rest_framework.test import APITestCase
from src.utils.fakers import WishFactory


class SubmitRequestAPIViewTestCase(APITestCase):
    def test_legacy_url_supports_secure_guest_reservation(self):
        wish = WishFactory()
        response = self.client.post(
            reverse("submit_request", args=[wish.id]),
            {
                **{
                    "purchase_by": (date.today() + timedelta(days=2)).isoformat(),
                    "purchase_plan": "Order the exact item online",
                    "details_checked": True,
                },
                "nickname": "Sam",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["data"]["wish_id"], str(wish.id))
        self.assertTrue(response.data["data"]["management_token"])

    def test_legacy_url_rejects_unverified_friend_ids(self):
        wish = WishFactory()
        response = self.client.post(
            reverse("submit_request", args=[wish.id]),
            {"friend": str(wish.wishlist.profile_id)},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
