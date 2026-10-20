from datetime import date, timedelta

from django.urls import reverse
from rest_framework.test import APITestCase

from src.apps.wishlist.models import Wish, Wishlist
from src.utils.fakers import ProfileFactory, UserFactory, WishFactory, WishlistFactory


class DomainContractAPITests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = ProfileFactory(profile_id=self.user.id)
        self.other_profile = ProfileFactory()
        self.wishlist = WishlistFactory(profile=self.profile)
        self.wish = WishFactory(wishlist=self.wishlist)
        self.client.force_authenticate(user=self.user)

    def test_create_wishlist_uses_authenticated_actor(self):
        response = self.client.post(
            reverse("wishlist"),
            {
                "profile": str(self.other_profile.profile_id),
                "name": "Books",
                "description": "Novels",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        item = Wishlist.objects.get(id=response.data["data"]["id"])
        self.assertEqual(item.profile_id, self.profile.profile_id)

    def test_patch_cannot_reassign_wishlist_owner(self):
        response = self.client.patch(
            reverse("wishlist_action", args=[self.wishlist.id]),
            {"profile": str(self.other_profile.profile_id), "name": "New"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.wishlist.refresh_from_db()
        self.assertEqual(self.wishlist.profile_id, self.profile.profile_id)

    def test_wish_body_cannot_override_url_parent(self):
        other = WishlistFactory(profile=self.profile)
        response = self.client.patch(
            reverse("wish_action", args=[self.wishlist.id, self.wish.id]),
            {"wishlist": str(other.id), "name": "New"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.wish.refresh_from_db()
        self.assertEqual(self.wish.wishlist_id, self.wishlist.id)

    def test_cannot_delete_wish_through_other_owned_parent(self):
        other = WishlistFactory(profile=self.profile)
        response = self.client.delete(
            reverse("wish_action", args=[other.id, self.wish.id])
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue(Wish.objects.filter(id=self.wish.id).exists())

    def test_cannot_patch_wish_through_other_owned_parent(self):
        other = WishlistFactory(profile=self.profile)
        response = self.client.patch(
            reverse("wish_action", args=[other.id, self.wish.id]),
            {"name": "Hijack"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.wish.refresh_from_db()
        self.assertNotEqual(self.wish.name, "Hijack")

    def test_malformed_uuid_is_400(self):
        response = self.client.get(reverse("wish_by_id", args=["not-a-uuid"]))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error_type"], ["INVALID_ID"])

    def test_reservation_requires_business_actor(self):
        response = self.client.post(
            reverse("submit_request", args=[self.wish.id]),
            {
                "purchase_by": (date.today() + timedelta(days=2)).isoformat(),
                "purchase_plan": "Order the exact item online",
                "details_checked": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)
