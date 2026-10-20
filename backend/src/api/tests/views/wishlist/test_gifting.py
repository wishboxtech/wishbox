from datetime import date, timedelta

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest import skipUnless
from unittest.mock import patch
from uuid import uuid4

from django.db import close_old_connections, connection
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from src.apps.wishlist.dto.gifting import ReserveGiftInputDTO
from src.apps.wishlist.models import Notification, ReservationRequest, WishInteraction
from src.core.composition import gifting_service
from src.apps.wishlist.domain.gifting import GiftConflict
from src.utils.fakers import UserFactory, ProfileFactory, WishlistFactory, WishFactory


class GiftingAPITests(APITestCase):
    def setUp(self):
        self.owner = UserFactory()
        self.profile = ProfileFactory(profile_id=self.owner.id)
        self.giver = UserFactory()
        ProfileFactory(profile_id=self.giver.id)
        self.wishlist = WishlistFactory(profile=self.profile)
        self.wish = WishFactory(wishlist=self.wishlist)
        self.reserve_url = reverse("wish_reservation", args=[self.wish.id])
        self.activity_url = reverse("wish_activity", args=[self.wish.id])
        self.visitor = {"HTTP_X_WISHY_VISITOR": str(uuid4())}

    def reserve_guest(self):
        response = self.client.post(
            self.reserve_url,
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
        self.assertEqual(response.status_code, 201, response.data)
        return response.data["data"]["management_token"]

    def test_guest_full_lifecycle_and_owner_confirmation(self):
        token = self.reserve_guest()
        item = ReservationRequest.objects.get(wish=self.wish)
        self.assertNotEqual(item.management_hash, token)
        self.assertEqual(len(item.management_hash), 64)
        self.assertEqual(
            Notification.objects.filter(profile=self.profile, event="reserved").count(),
            1,
        )
        response = self.client.patch(
            self.reserve_url,
            {"action": "purchase"},
            format="json",
            HTTP_X_WISHY_GIFT_TOKEN=token,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["status"], "purchased")
        response = self.client.patch(
            self.reserve_url,
            {"action": "receive"},
            format="json",
            HTTP_X_WISHY_GIFT_TOKEN=token,
        )
        self.assertEqual(response.status_code, 403)
        self.client.force_authenticate(self.owner)
        response = self.client.patch(
            self.reserve_url, {"action": "receive"}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["status"], "received")
        self.client.force_authenticate(None)
        self.assertEqual(
            self.client.post(
                self.reserve_url,
                {
                    **{
                        "purchase_by": (date.today() + timedelta(days=2)).isoformat(),
                        "purchase_plan": "Order the exact item online",
                        "details_checked": True,
                    },
                    "nickname": "Other",
                },
                format="json",
            ).status_code,
            409,
        )
        response = self.client.patch(
            self.reserve_url,
            {"action": "cancel"},
            format="json",
            HTTP_X_WISHY_GIFT_TOKEN=token,
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(Notification.objects.filter(profile=self.profile).count(), 3)

    def test_cannot_change_someone_elses_gift_or_forge_actor(self):
        self.reserve_guest()
        for action in ("purchase", "cancel", "receive"):
            response = self.client.patch(
                self.reserve_url,
                {"action": action},
                format="json",
                HTTP_X_WISHY_GIFT_TOKEN="forged",
            )
            self.assertEqual(response.status_code, 403)
        self.client.force_authenticate(self.giver)
        response = self.client.patch(
            self.reserve_url, {"action": "purchase"}, format="json"
        )
        self.assertEqual(response.status_code, 403)
        other_wish = WishFactory(wishlist=self.wishlist)
        response = self.client.post(
            reverse("submit_request", args=[other_wish.id]),
            {"friend": str(self.owner.id)},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(ReservationRequest.objects.filter(wish=other_wish).exists())

    def test_owner_cannot_reserve_self_or_confirm_before_purchase(self):
        self.client.force_authenticate(self.owner)
        self.assertEqual(
            self.client.post(
                self.reserve_url,
                {
                    "purchase_by": (date.today() + timedelta(days=2)).isoformat(),
                    "purchase_plan": "Order the exact item online",
                    "details_checked": True,
                },
                format="json",
            ).status_code,
            403,
        )
        self.client.force_authenticate(None)
        self.reserve_guest()
        self.client.force_authenticate(self.owner)
        self.assertEqual(
            self.client.patch(
                self.reserve_url, {"action": "receive"}, format="json"
            ).status_code,
            409,
        )

    def test_cancel_releases_and_stale_token_cannot_control_new_reservation(self):
        old_token = self.reserve_guest()
        self.assertEqual(
            self.client.post(
                self.reserve_url,
                {
                    **{
                        "purchase_by": (date.today() + timedelta(days=2)).isoformat(),
                        "purchase_plan": "Order the exact item online",
                        "details_checked": True,
                    },
                    "nickname": "Other",
                },
                format="json",
            ).status_code,
            409,
        )
        response = self.client.patch(
            self.reserve_url,
            {"action": "cancel"},
            format="json",
            HTTP_X_WISHY_GIFT_TOKEN=old_token,
        )
        self.assertEqual(response.status_code, 200)
        self.wish.refresh_from_db()
        self.assertIsNone(self.wish.accepted_request_id)
        new_token = self.reserve_guest()
        self.assertNotEqual(old_token, new_token)
        self.assertEqual(
            self.client.patch(
                self.reserve_url,
                {"action": "purchase"},
                format="json",
                HTTP_X_WISHY_GIFT_TOKEN=old_token,
            ).status_code,
            403,
        )

    def test_unique_views_likes_and_unlikes(self):
        for _ in range(3):
            response = self.client.post(
                self.activity_url, {"action": "view"}, format="json", **self.visitor
            )
        self.assertEqual(response.data["data"]["views"], 1)
        for _ in range(2):
            response = self.client.post(
                self.activity_url, {"action": "like"}, format="json", **self.visitor
            )
        self.assertEqual(response.data["data"]["likes"], 1)
        self.assertTrue(response.data["data"]["liked"])
        response = self.client.post(
            self.activity_url, {"action": "unlike"}, format="json", **self.visitor
        )
        self.assertEqual(response.data["data"]["likes"], 0)
        self.assertEqual(WishInteraction.objects.count(), 1)
        other = {"HTTP_X_WISHY_VISITOR": str(uuid4())}
        response = self.client.post(
            self.activity_url, {"action": "view"}, format="json", **other
        )
        self.assertEqual(response.data["data"]["views"], 2)

    def test_account_activity_deduplicates_across_browser_ids(self):
        self.client.force_authenticate(self.giver)
        for _ in range(2):
            response = self.client.post(
                self.activity_url,
                {"action": "view"},
                format="json",
                HTTP_X_WISHY_VISITOR=str(uuid4()),
            )
        self.assertEqual(response.data["data"]["views"], 1)

    def test_public_state_hides_credentials_and_actor_ids(self):
        token = self.reserve_guest()
        response = self.client.get(self.activity_url, **self.visitor)
        data = response.data["data"]
        self.assertEqual(data["status"], "reserved")
        self.assertFalse(data["is_giver"])
        self.assertNotIn("management_hash", str(data))
        self.assertNotIn(token, str(data))
        response = self.client.get(
            self.activity_url, **self.visitor, HTTP_X_WISHY_GIFT_TOKEN=token
        )
        self.assertTrue(response.data["data"]["is_giver"])
        self.assertFalse(
            self.client.get(
                self.activity_url, **self.visitor, HTTP_X_WISHY_GIFT_TOKEN="wrong"
            ).data["data"]["is_giver"]
        )

    def test_inbox_ownership_read_one_and_read_all(self):
        self.reserve_guest()
        notice = Notification.objects.get(profile=self.profile)
        self.client.force_authenticate(self.giver)
        url = reverse("notifications")
        self.assertEqual(self.client.get(url).data["data"]["unread"], 0)
        self.client.patch(url, {"notification_id": str(notice.id)}, format="json")
        notice.refresh_from_db()
        self.assertIsNone(notice.read_at)
        self.client.force_authenticate(self.owner)
        self.assertEqual(self.client.get(url).data["data"]["unread"], 1)
        response = self.client.patch(url, {}, format="json")
        self.assertEqual(response.data["data"]["unread"], 0)
        self.assertIsNotNone(response.data["data"]["items"][0]["read_at"])
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get(url).status_code, 401)

    def test_registered_gifts_are_private_and_receive_sends_thank_you(self):
        self.client.force_authenticate(self.giver)
        response = self.client.post(
            self.reserve_url,
            {
                "purchase_by": (date.today() + timedelta(days=2)).isoformat(),
                "purchase_plan": "Order the exact item online",
                "details_checked": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(self.client.get(reverse("my_gifts")).data["data"]), 1)
        self.client.patch(self.reserve_url, {"action": "purchase"}, format="json")
        self.client.force_authenticate(self.owner)
        self.assertEqual(self.client.get(reverse("my_gifts")).data["data"], [])
        self.client.patch(self.reserve_url, {"action": "receive"}, format="json")
        self.assertEqual(
            Notification.objects.filter(
                profile_id=self.giver.id, event="gift_received"
            ).count(),
            1,
        )

    def test_shared_metadata_and_batch_activity(self):
        WishFactory.create_batch(4, wishlist=self.wishlist)
        url = reverse("shared_wishlist", args=[self.wishlist.id])
        with self.assertNumQueries(7):
            response = self.client.get(url, **self.visitor)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["wishlist"]["name"], self.wishlist.name)
        self.assertEqual(len(response.data["data"]["activity"]), 5)
        self.assertFalse(response.data["data"]["is_owner"])

    def test_missing_shared_list_and_wish_activity_are_404(self):
        self.assertEqual(
            self.client.get(
                reverse("shared_wishlist", args=[uuid4()]), **self.visitor
            ).status_code,
            404,
        )
        self.assertEqual(
            self.client.get(
                reverse("wish_activity", args=[uuid4()]), **self.visitor
            ).status_code,
            404,
        )

    def test_activity_rejects_non_object_and_null_actions(self):
        for data in ([], {"action": None}, {}):
            response = self.client.post(
                self.activity_url, data, format="json", **self.visitor
            )
            self.assertEqual(response.status_code, 400)

    def test_name_only_lists_empty_descriptions_and_non_negative_price(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(
            reverse("wishlist"), {"name": "Hints"}, format="json"
        )
        self.assertEqual(response.status_code, 201)
        parent = response.data["data"]["id"]
        url = reverse("wishlist_action", args=[parent])
        response = self.client.post(url, {"name": "Book", "price": "0"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["data"]["description"], "")
        self.assertEqual(response.data["data"]["wishlist_id"], parent)
        response = self.client.post(url, {"name": "Book", "price": "-1"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_inbox_read_one_does_not_read_other_notices(self):
        self.reserve_guest()
        second = Notification.objects.create(
            profile=self.profile,
            wish=self.wish,
            wish_name=self.wish.name,
            event="purchased",
        )
        self.client.force_authenticate(self.owner)
        response = self.client.patch(
            reverse("notifications"), {"notification_id": str(second.id)}, format="json"
        )
        self.assertEqual(response.data["data"]["unread"], 1)
        second.refresh_from_db()
        self.assertIsNotNone(second.read_at)

    def test_failed_notification_rolls_back_reservation(self):
        with patch(
            "src.apps.wishlist.repositories.gifting.DjangoGiftRepository.notify",
            side_effect=RuntimeError("write failed"),
        ):
            with self.assertRaises(RuntimeError):
                gifting_service().reserve(
                    ReserveGiftInputDTO(
                        wish_id=self.wish.id,
                        nickname="Sam",
                        **{
                            "purchase_by": (
                                date.today() + timedelta(days=2)
                            ).isoformat(),
                            "purchase_plan": "Order the exact item online",
                            "details_checked": True,
                        }
                    )
                )
        self.assertFalse(ReservationRequest.objects.filter(wish=self.wish).exists())
        self.wish.refresh_from_db()
        self.assertIsNone(self.wish.accepted_request_id)

    def test_invalid_visitor_action_and_token_inputs(self):
        self.assertEqual(self.client.get(self.activity_url).status_code, 400)
        self.assertEqual(
            self.client.post(
                self.activity_url, {"action": "invalid"}, format="json", **self.visitor
            ).status_code,
            400,
        )
        self.assertEqual(
            self.client.post(
                self.reserve_url, {"nickname": "   "}, format="json"
            ).status_code,
            400,
        )


@skipUnless(connection.vendor == "postgresql", "PostgreSQL row locks required")
class ConcurrentGiftingTests(TransactionTestCase):
    def test_only_one_simultaneous_reservation_succeeds(self):
        wishlist = WishlistFactory()
        wish = WishFactory(wishlist=wishlist)
        barrier = Barrier(2)

        def reserve():
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                gifting_service().reserve(
                    ReserveGiftInputDTO(
                        wish_id=wish.id,
                        nickname="Friend",
                        **{
                            "purchase_by": (
                                date.today() + timedelta(days=2)
                            ).isoformat(),
                            "purchase_plan": "Order the exact item online",
                            "details_checked": True,
                        }
                    )
                )
                return "reserved"
            except GiftConflict:
                return "conflict"
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: reserve(), range(2)))
        self.assertCountEqual(results, ["reserved", "conflict"])
        self.assertEqual(
            ReservationRequest.objects.filter(wish=wish, status="reserved").count(), 1
        )
        self.assertEqual(Notification.objects.filter(wish=wish).count(), 1)
