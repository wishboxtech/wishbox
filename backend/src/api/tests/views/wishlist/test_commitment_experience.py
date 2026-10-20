from datetime import timedelta
from unittest.mock import patch
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest import skipUnless

from django.db import close_old_connections, connection
from django.test import TransactionTestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from src.apps.wishlist.dto.gifting import ReserveGiftInputDTO, SaveExperienceInputDTO
from src.apps.wishlist.models import Notification, ReservationRequest
from src.core.composition import gifting_service
from src.utils.fakers import UserFactory, ProfileFactory, WishlistFactory, WishFactory


class CommitmentExperienceAPITests(APITestCase):
    def setUp(self):
        self.now = timezone.now()
        clock = patch("src.core.composition.now", side_effect=lambda: self.now)
        clock.start()
        self.addCleanup(clock.stop)
        self.owner, self.giver, self.other = UserFactory(), UserFactory(), UserFactory()
        for user in (self.owner, self.giver, self.other):
            ProfileFactory(profile_id=user.id)
        self.wishlist = WishlistFactory(profile_id=self.owner.id)
        self.wish = WishFactory(wishlist=self.wishlist)
        self.url = reverse("wish_reservation", args=[self.wish.id])
        self.visitor = {"HTTP_X_WISHY_VISITOR": str(uuid4())}

    def plan(self, days=2):
        return {
            "purchase_by": (self.now.date() + timedelta(days=days)).isoformat(),
            "purchase_plan": "Order the exact model after work",
            "details_checked": True,
        }

    def reserve(self, registered=True):
        self.client.force_authenticate(self.giver if registered else None)
        response = self.client.post(
            self.url, {**self.plan(), "nickname": "Sam"}, format="json"
        )
        self.assertEqual(response.status_code, 201, response.data)
        data = response.data["data"]
        self.gift_id = data["id"]
        self.token = data["management_token"]
        self.experience_url = reverse("gift_experience", args=[self.gift_id])
        return data

    def receive(self, registered=True):
        self.reserve(registered)
        response = self.client.patch(
            self.url,
            {"action": "purchase"},
            format="json",
            HTTP_X_WISHY_GIFT_TOKEN=self.token,
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.client.force_authenticate(self.owner)
        response = self.client.patch(self.url, {"action": "receive"}, format="json")
        self.assertEqual(response.status_code, 200, response.data)
        self.assertIsNone(response.data["data"]["purchase_by"])

    def test_reservation_requires_a_real_plan_and_checked_details(self):
        self.client.force_authenticate(self.giver)
        for payload in (
            {},
            {**self.plan(), "details_checked": False},
            {
                **self.plan(),
                "purchase_by": (self.now.date() - timedelta(days=1)).isoformat(),
            },
            {
                **self.plan(),
                "purchase_by": (self.now.date() + timedelta(days=31)).isoformat(),
            },
            {**self.plan(), "purchase_plan": "  "},
        ):
            self.assertEqual(
                self.client.post(self.url, payload, format="json").status_code, 400
            )
        self.assertEqual(ReservationRequest.objects.count(), 0)

    def test_private_plan_and_public_reservation_identity(self):
        data = self.reserve()
        self.assertEqual(data["purchase_plan"], self.plan()["purchase_plan"])
        self.assertIsNotNone(data["expires_at"])
        gift = ReservationRequest.objects.get(id=self.gift_id)
        self.assertTrue(gift.details_checked)
        self.assertGreater(gift.expires_at.date(), gift.purchase_by)
        self.client.force_authenticate(None)
        public = self.client.get(
            reverse("wish_activity", args=[self.wish.id]), **self.visitor
        ).data["data"]
        self.assertIsNone(public["reservation_id"])
        self.assertNotIn("purchase_plan", public)
        self.client.force_authenticate(self.owner)
        owner = self.client.get(self.experience_url).data["data"]
        self.assertEqual(owner["role"], "owner")
        self.assertNotIn("purchase_by", owner["gift"])

    def test_automatic_expiry_releases_a_wish_and_notifies_once(self):
        self.reserve()
        gift = ReservationRequest.objects.get(id=self.gift_id)
        self.now = gift.expires_at + timedelta(seconds=1)
        self.client.force_authenticate(None)
        response = self.client.get(
            reverse("wish_activity", args=[self.wish.id]), **self.visitor
        )
        self.assertEqual(response.data["data"]["status"], "available")
        gifting_service().maintain(reminders=True)
        gift.refresh_from_db()
        self.assertEqual(gift.status, "expired")
        self.assertEqual(
            Notification.objects.filter(
                event="hold_released", profile_id=self.owner.id
            ).count(),
            1,
        )
        self.assertEqual(
            Notification.objects.filter(
                event="hold_expired", profile_id=self.giver.id
            ).count(),
            1,
        )
        self.wish.refresh_from_db()
        self.assertIsNone(self.wish.accepted_request_id)
        self.client.force_authenticate(self.giver)
        self.assertEqual(
            self.client.patch(
                self.url, {"action": "purchase"}, format="json"
            ).status_code,
            409,
        )
        self.assertEqual(
            self.client.post(self.url, self.plan(), format="json").status_code, 201
        )

    def test_reminder_goes_only_to_giver_and_only_once(self):
        self.reserve()
        gift = ReservationRequest.objects.get(id=self.gift_id)
        self.now = gift.reminder_at + timedelta(seconds=1)
        self.assertEqual(gifting_service().maintain(reminders=True).reminded, 1)
        self.assertEqual(gifting_service().maintain(reminders=True).reminded, 0)
        self.assertEqual(
            Notification.objects.filter(
                event="plan_reminder", profile_id=self.giver.id
            ).count(),
            1,
        )
        self.assertEqual(
            Notification.objects.filter(
                event="plan_reminder", profile_id=self.owner.id
            ).count(),
            0,
        )

    def test_guest_can_read_expired_plan_without_receiving_fake_reminder(self):
        self.reserve(registered=False)
        gift = ReservationRequest.objects.get(id=self.gift_id)
        self.now = gift.reminder_at + timedelta(seconds=1)
        gifting_service().maintain(reminders=True)
        self.assertEqual(Notification.objects.filter(event="plan_reminder").count(), 0)
        self.now = gift.expires_at + timedelta(seconds=1)
        response = self.client.get(
            self.experience_url, HTTP_X_WISHY_GIFT_TOKEN=self.token
        )
        self.assertEqual(response.data["data"]["gift"]["status"], "expired")

    def test_purchased_gifts_do_not_expire(self):
        self.reserve()
        self.client.patch(self.url, {"action": "purchase"}, format="json")
        self.now += timedelta(days=40)
        self.assertEqual(gifting_service().maintain(reminders=True).expired, 0)
        self.assertEqual(
            ReservationRequest.objects.get(id=self.gift_id).status, "purchased"
        )

    def test_only_giver_can_reschedule_once_with_a_bounded_extension(self):
        self.reserve()
        new_day = (self.now.date() + timedelta(days=5)).isoformat()
        self.client.force_authenticate(self.owner)
        self.assertEqual(
            self.client.patch(
                self.url,
                {"action": "reschedule", "purchase_by": new_day},
                format="json",
            ).status_code,
            403,
        )
        self.client.force_authenticate(self.giver)
        for day in (
            None,
            (self.now.date() + timedelta(days=1)).isoformat(),
            (self.now.date() + timedelta(days=10)).isoformat(),
        ):
            self.assertEqual(
                self.client.patch(
                    self.url,
                    {"action": "reschedule", "purchase_by": day},
                    format="json",
                ).status_code,
                400,
            )
        response = self.client.patch(
            self.url, {"action": "reschedule", "purchase_by": new_day}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["extension_count"], 1)
        self.assertEqual(
            self.client.patch(
                self.url,
                {"action": "reschedule", "purchase_by": new_day},
                format="json",
            ).status_code,
            409,
        )

    def test_private_dissatisfaction_never_changes_giver_or_public_responses(self):
        self.receive()
        self.client.force_authenticate(self.giver)
        before = self.client.get(self.experience_url).data["data"]
        self.client.force_authenticate(self.owner)
        before_notifications = Notification.objects.count()
        response = self.client.patch(
            self.experience_url,
            {
                "action": "save_private",
                "fit": "not_for_me",
                "private_note": "A private fit issue",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["private_note"], "A private fit issue")
        self.assertEqual(Notification.objects.count(), before_notifications)
        self.client.force_authenticate(self.giver)
        self.assertEqual(self.client.get(self.experience_url).data["data"], before)
        for data in (
            self.client.get(reverse("my_gifts")).data["data"],
            self.client.get(self.experience_url).data["data"],
        ):
            self.assertNotIn("private_note", str(data))
            self.assertNotIn("not_for_me", str(data))
            self.assertNotIn("A private fit issue", str(data))
        self.client.force_authenticate(None)
        public = self.client.get(
            reverse("wish_activity", args=[self.wish.id]), **self.visitor
        ).data["data"]
        self.assertEqual(public["status"], "received")
        self.assertNotIn("fit", public)

    def test_feedback_is_optional_and_can_be_changed_after_using_the_gift(self):
        self.receive()
        gift = ReservationRequest.objects.get(id=self.gift_id)
        self.assertEqual(gift.fit, "")
        self.assertEqual(gift.thank_you, "")
        for fit in ("trying", "adjust", "fits", None):
            response = self.client.patch(
                self.experience_url,
                {"action": "save_private", "fit": fit},
                format="json",
            )
            self.assertEqual(response.status_code, 200)
        self.assertEqual(ReservationRequest.objects.get(id=self.gift_id).fit, "")

    def test_feedback_and_shared_notes_require_confirmed_arrival(self):
        self.reserve()
        self.client.force_authenticate(self.owner)
        for data in (
            {"action": "save_private", "fit": "fits"},
            {"action": "share_thanks", "thank_you": "Thanks"},
        ):
            self.assertEqual(
                self.client.patch(self.experience_url, data, format="json").status_code,
                409,
            )

    def test_guest_and_unrelated_user_cannot_read_private_experience(self):
        self.receive(registered=False)
        self.client.patch(
            self.experience_url,
            {
                "action": "save_private",
                "fit": "adjust",
                "private_note": "Private size note",
            },
            format="json",
        )
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get(self.experience_url).status_code, 404)
        self.assertEqual(
            self.client.get(
                self.experience_url, HTTP_X_WISHY_GIFT_TOKEN="wrong"
            ).status_code,
            404,
        )
        response = self.client.get(
            self.experience_url, HTTP_X_WISHY_GIFT_TOKEN=self.token
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Private size note", str(response.data))
        self.assertEqual(
            self.client.patch(
                self.experience_url,
                {"action": "save_private", "fit": "fits"},
                format="json",
                HTTP_X_WISHY_GIFT_TOKEN=self.token,
            ).status_code,
            403,
        )
        self.client.force_authenticate(self.other)
        self.assertEqual(self.client.get(self.experience_url).status_code, 404)
        self.assertEqual(
            self.client.patch(
                self.experience_url,
                {"action": "share_thanks", "thank_you": "Forged"},
                format="json",
            ).status_code,
            404,
        )

    def test_thank_you_is_shared_only_explicitly_and_can_be_withdrawn(self):
        self.receive()
        self.assertEqual(Notification.objects.filter(event="thanks_shared").count(), 0)
        self.assertEqual(
            self.client.patch(
                self.experience_url,
                {"action": "share_thanks", "thank_you": " "},
                format="json",
            ).status_code,
            400,
        )
        data = {
            "action": "share_thanks",
            "thank_you": "Our next reading afternoon is sorted.",
        }
        for _ in range(2):
            self.assertEqual(
                self.client.patch(self.experience_url, data, format="json").status_code,
                200,
            )
        self.assertEqual(
            Notification.objects.filter(
                profile_id=self.giver.id, event="thanks_shared"
            ).count(),
            1,
        )
        self.client.force_authenticate(self.giver)
        self.assertEqual(
            self.client.get(self.experience_url).data["data"]["gift"]["thank_you"],
            data["thank_you"],
        )
        self.client.force_authenticate(self.owner)
        self.client.patch(
            self.experience_url, {"action": "withdraw_thanks"}, format="json"
        )
        self.client.force_authenticate(self.giver)
        self.assertEqual(
            self.client.get(self.experience_url).data["data"]["gift"]["thank_you"], ""
        )
        self.assertEqual(
            ReservationRequest.objects.get(id=self.gift_id).status, "received"
        )

    def test_practical_follow_up_is_explicit_and_acknowledged_without_a_rating(self):
        self.receive()
        self.client.patch(
            self.experience_url,
            {
                "action": "save_private",
                "fit": "adjust",
                "private_note": "Do not share this sentence",
            },
            format="json",
        )
        response = self.client.patch(
            self.experience_url,
            {
                "action": "share_follow_up",
                "follow_up_note": "Could we check the size together?",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Notification.objects.filter(
                event="follow_up_shared", profile_id=self.giver.id
            ).count(),
            1,
        )
        self.assertEqual(
            self.client.patch(
                self.experience_url, {"action": "acknowledge_follow_up"}, format="json"
            ).status_code,
            403,
        )
        self.client.force_authenticate(self.giver)
        data = self.client.get(self.experience_url).data["data"]
        self.assertIn("check the size", data["gift"]["follow_up_note"])
        self.assertNotIn("Do not share", str(data))
        for _ in range(2):
            self.assertEqual(
                self.client.patch(
                    self.experience_url,
                    {"action": "acknowledge_follow_up"},
                    format="json",
                ).status_code,
                200,
            )
        self.assertEqual(
            Notification.objects.filter(
                event="follow_up_seen", profile_id=self.owner.id
            ).count(),
            1,
        )
        self.client.force_authenticate(self.owner)
        self.client.patch(
            self.experience_url, {"action": "withdraw_follow_up"}, format="json"
        )
        self.client.force_authenticate(self.giver)
        self.assertEqual(
            self.client.get(self.experience_url).data["data"]["gift"]["follow_up_note"],
            "",
        )

    def test_notification_failure_rolls_back_shared_note(self):
        self.receive()
        with patch(
            "src.apps.wishlist.repositories.gifting.DjangoGiftRepository.notify",
            side_effect=RuntimeError("write failed"),
        ):
            with self.assertRaises(RuntimeError):
                gifting_service().save_experience(
                    SaveExperienceInputDTO(
                        reservation_id=self.gift_id,
                        profile_id=self.owner.id,
                        action="share_thanks",
                        thank_you="Thanks for reading with me",
                    )
                )
        self.assertEqual(ReservationRequest.objects.get(id=self.gift_id).thank_you, "")


@skipUnless(connection.vendor == "postgresql", "PostgreSQL row locks required")
class ConcurrentMaintenanceTests(TransactionTestCase):
    def test_parallel_maintenance_expires_and_notifies_only_once(self):
        wish = WishFactory()
        data = ReserveGiftInputDTO(
            wish_id=wish.id,
            nickname="Sam",
            purchase_by=timezone.now().date(),
            purchase_plan="Visit the bookshop",
            details_checked=True,
        )
        output = gifting_service().reserve(data)
        ReservationRequest.objects.filter(id=output.id).update(
            expires_at=timezone.now() - timedelta(seconds=1)
        )
        barrier = Barrier(2)

        def maintain():
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                return gifting_service().maintain(reminders=True).expired
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as pool:
            result = list(pool.map(lambda _: maintain(), range(2)))
        self.assertEqual(sum(result), 1)
        self.assertEqual(
            Notification.objects.filter(wish=wish, event="hold_released").count(), 1
        )
        self.assertEqual(ReservationRequest.objects.get(id=output.id).status, "expired")
