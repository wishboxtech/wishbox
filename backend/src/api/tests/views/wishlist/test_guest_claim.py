from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from threading import Barrier
from unittest import skipUnless
from unittest.mock import patch

from django.db import close_old_connections, connection
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from src.apps.authentication.dto import VerifiedOTPOutputDTO
from src.apps.authentication.models import User
from src.apps.wishlist.models import GuestIdentity, ReservationRequest
from src.core.composition import gifting_service
from src.apps.wishlist.repositories.credentials import SecureGiftCredentials
from src.apps.wishlist.repositories.guest import DjangoGuestRepository
from src.shared.transactions import transaction_boundary
from src.utils.fakers import UserFactory, ProfileFactory, WishlistFactory, WishFactory


class GuestSignupTests(APITestCase):
    def setUp(self):
        self.owner = UserFactory()
        self.owner_profile = ProfileFactory(profile_id=self.owner.id)
        self.wishlist = WishlistFactory(profile=self.owner_profile)
        self.wish = WishFactory(wishlist=self.wishlist)
        self.key = "a" * 64
        self.url = reverse("wish_reservation", args=[self.wish.id])
        response = self.client.post(
            self.url,
            {
                "nickname": "Guest",
                "purchase_by": (date.today() + timedelta(days=3)).isoformat(),
                "purchase_plan": "Order the exact item online",
                "details_checked": True,
                "guest_key": self.key,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201, response.data)
        self.token = response.data["data"]["management_token"]

    def login(self, phone, key=None):
        with patch(
            "src.apps.authentication.repositories.otp.CachedOTPRepository.verify",
            return_value=VerifiedOTPOutputDTO(identifier=phone, state="phone_number"),
        ):
            return self.client.post(
                reverse("verify_otp"),
                {
                    "otp_id": "verified",
                    "otp_code": "123456",
                    **({"guest_key": key} if key else {}),
                },
                format="json",
            )

    def test_first_signup_claims_guest_and_revokes_browser_gift_token(self):
        response = self.login("09123450001", self.key)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertTrue(response.data["data"]["is_new_user"])
        self.assertTrue(response.data["data"]["guest_claimed"])
        identity = GuestIdentity.objects.get()
        self.assertNotEqual(identity.key_hash, self.key)
        self.assertEqual(identity.claimed_user.phone_number, "09123450001")
        self.assertIsNotNone(identity.consumed_at)
        self.assertEqual(
            self.client.patch(
                self.url,
                {"action": "purchase"},
                format="json",
                HTTP_X_WISHY_GIFT_TOKEN=self.token,
            ).status_code,
            403,
        )
        self.client.force_authenticate(identity.claimed_user)
        self.assertEqual(
            self.client.patch(
                self.url, {"action": "purchase"}, format="json"
            ).status_code,
            200,
        )
        gifts = self.client.get(reverse("my_gifts")).data["data"]
        self.assertEqual(len(gifts), 1)
        self.assertNotIn("management_hash", gifts[0])
        self.assertNotIn("guest_key", str(gifts))
        # A newly created user may receive a gift before completing their profile.
        self.client.force_authenticate(self.owner)
        self.assertEqual(
            self.client.patch(
                self.url, {"action": "receive"}, format="json"
            ).status_code,
            200,
        )

    def test_existing_account_cannot_claim_even_with_valid_browser_key(self):
        UserFactory(phone_number="09123450002")
        response = self.login("09123450002", self.key)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertFalse(response.data["data"]["is_new_user"])
        self.assertFalse(response.data["data"]["guest_claimed"])
        self.assertIsNone(GuestIdentity.objects.get().consumed_at)

    def test_first_signup_without_consent_does_not_link(self):
        response = self.login("09123450003")
        self.assertFalse(response.data["data"]["guest_claimed"])
        response = self.login("09123450003", self.key)
        self.assertFalse(response.data["data"]["guest_claimed"])
        self.assertIsNone(GuestIdentity.objects.get().claimed_user_id)

    def test_browser_identity_cannot_move_to_another_new_account(self):
        self.login("09123450004", self.key)
        response = self.login("09123450005", self.key)
        self.assertFalse(response.data["data"]["guest_claimed"])
        self.assertEqual(
            GuestIdentity.objects.get().claimed_user.phone_number, "09123450004"
        )

    def test_wrong_key_does_not_grant_access_or_claim(self):
        response = self.login("09123450006", "b" * 64)
        self.assertFalse(response.data["data"]["guest_claimed"])
        self.client.force_authenticate(User.objects.get(phone_number="09123450006"))
        self.assertEqual(
            self.client.patch(
                self.url, {"action": "purchase"}, format="json"
            ).status_code,
            403,
        )

    def test_reused_consumed_browser_cannot_attach_later_guest_gifts(self):
        self.login("09123450007", self.key)
        new_wish = WishFactory(wishlist=self.wishlist)
        response = self.client.post(
            reverse("wish_reservation", args=[new_wish.id]),
            {
                "nickname": "Another guest",
                "purchase_by": (date.today() + timedelta(days=2)).isoformat(),
                "purchase_plan": "Arrange the gift directly",
                "details_checked": True,
                "guest_key": self.key,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertIsNone(
            ReservationRequest.objects.get(wish=new_wish).guest_identity_id
        )


@skipUnless(connection.vendor == "postgresql", "PostgreSQL row locks required")
class GuestClaimConcurrencyTests(TransactionTestCase):
    def test_only_one_concurrent_signup_claims_a_browser(self):
        identity = GuestIdentity.objects.create(
            key_hash=SecureGiftCredentials().digest("a" * 64)
        )
        users = [UserFactory(), UserFactory()]
        barrier = Barrier(2)

        def claim(user):
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                with transaction_boundary():
                    return DjangoGuestRepository().claim(identity.key_hash, user.id)
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(claim, users))
        self.assertEqual(sorted(results), [False, True])
