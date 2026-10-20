from contextlib import nullcontext
from datetime import date, datetime, timedelta, timezone
from unittest import TestCase
from unittest.mock import Mock
from uuid import uuid4

from src.apps.wishlist.domain import Wish, Wishlist
from src.apps.wishlist.domain.gifting import (
    GiftConflict,
    GiftForbidden,
    next_gift_status,
)
from src.apps.wishlist.dto.gifting import (
    ChangeGiftInputDTO,
    GiftRecordOutputDTO,
    ReserveGiftInputDTO,
)
from src.apps.wishlist.services.gifting import GiftingService


class GiftingPolicyTests(TestCase):
    def test_lifecycle_and_roles(self):
        self.assertEqual(
            next_gift_status("reserved", "purchase", owner=False, giver=True),
            "purchased",
        )
        self.assertEqual(
            next_gift_status("purchased", "receive", owner=True, giver=False),
            "received",
        )
        for state in ("reserved", "purchased"):
            self.assertEqual(
                next_gift_status(state, "cancel", owner=False, giver=True), "cancelled"
            )
        for state in ("received", "cancelled"):
            for action in ("purchase", "cancel"):
                with self.assertRaises(GiftConflict):
                    next_gift_status(state, action, owner=False, giver=True)
        with self.assertRaises(GiftConflict):
            next_gift_status("reserved", "receive", owner=True, giver=False)
        with self.assertRaises(GiftForbidden):
            next_gift_status("purchased", "receive", owner=False, giver=True)
        with self.assertRaises(GiftForbidden):
            next_gift_status("reserved", "cancel", owner=True, giver=False)

    def setUp(self):
        self.owner, self.giver, self.wish_id, self.list_id = (uuid4() for _ in range(4))
        self.repo, self.credentials, self.profiles = Mock(), Mock(), Mock()
        self.credentials.matches.return_value = False
        self.repo.candidates.return_value = ()
        self.service = GiftingService(
            self.repo,
            self.credentials,
            Mock(),
            self.profiles,
            nullcontext,
            lambda: datetime.now(timezone.utc),
        )
        now = datetime.now(timezone.utc)
        self.wish = Wish(
            self.wish_id, self.list_id, "Book", "", 100, None, None, now, now
        )
        self.repo.wish.return_value = self.wish
        self.repo.wishlist.return_value = Wishlist(
            self.list_id, self.owner, "Books", "", None, now, now
        )
        self.record = GiftRecordOutputDTO(
            id=1,
            wish_id=self.wish_id,
            wishlist_id=self.list_id,
            owner_id=self.owner,
            friend_id=self.giver,
            management_hash="hash",
            status="reserved",
            wish_name="Book",
            created_at=now,
        )
        self.repo.active.return_value = self.record

    def test_reserve_ownership_enforced_without_http(self):
        with self.assertRaises(GiftForbidden):
            self.service.reserve(
                ReserveGiftInputDTO(
                    wish_id=self.wish_id,
                    profile_id=self.owner,
                    **{
                        "purchase_by": (date.today() + timedelta(days=2)).isoformat(),
                        "purchase_plan": "Order the exact item online",
                        "details_checked": True,
                    }
                )
            )
        self.repo.reserve.assert_not_called()
        self.repo.wish.assert_called_once_with(self.wish_id, lock=True)

    def test_existing_reservation_is_conflict_without_http(self):
        with self.assertRaises(GiftConflict):
            self.service.reserve(
                ReserveGiftInputDTO(
                    wish_id=self.wish_id,
                    nickname="Sam",
                    **{
                        "purchase_by": (date.today() + timedelta(days=2)).isoformat(),
                        "purchase_plan": "Order the exact item online",
                        "details_checked": True,
                    }
                )
            )
        self.repo.reserve.assert_not_called()

    def test_update_actor_enforced_without_http(self):
        with self.assertRaises(GiftForbidden):
            self.service.change(
                ChangeGiftInputDTO(
                    wish_id=self.wish_id, profile_id=uuid4(), action="cancel"
                )
            )
        self.repo.change.assert_not_called()

    def test_registered_actor_does_not_need_guest_token(self):
        self.repo.change.return_value = self.record.model_copy(
            update={"status": "purchased"}
        )
        result = self.service.change(
            ChangeGiftInputDTO(
                wish_id=self.wish_id, profile_id=self.giver, action="purchase"
            )
        )
        self.assertEqual(result.status, "purchased")
        self.assertIsNone(result.management_token)
        self.repo.notify.assert_called_once_with(self.owner, self.wish, "purchased")
