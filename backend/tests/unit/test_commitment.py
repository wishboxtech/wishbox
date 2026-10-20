from datetime import date, datetime, timedelta, timezone
from unittest import TestCase
from unittest.mock import Mock
from contextlib import nullcontext
from uuid import uuid4
from src.apps.wishlist.domain.commitment import (
    require_purchase_date,
    require_extension,
    reservation_times,
)
from src.apps.wishlist.domain.gifting import GiftConflict, GiftForbidden
from src.apps.wishlist.dto.gifting import ReserveGiftInputDTO, SaveExperienceInputDTO
from src.apps.wishlist.services.gifting import GiftingService
from src.shared.domain.errors import DomainValidationError


class CommitmentPoliciesTests(TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 20, 12, tzinfo=timezone.utc)

    def test_date_bounds_and_buffer(self):
        for offset in (0, 1, 30):
            target = self.now.date() + timedelta(days=offset)
            require_purchase_date(target, self.now)
            expiry, reminder = reservation_times(target, self.now)
            self.assertGreater(expiry.date(), target)
            self.assertGreaterEqual(reminder, self.now + timedelta(hours=6))
            self.assertLess(reminder, expiry)
        for target in (
            None,
            self.now.date() - timedelta(days=1),
            self.now.date() + timedelta(days=31),
        ):
            with self.assertRaises(DomainValidationError):
                require_purchase_date(target, self.now)

    def test_bounded_single_extension(self):
        gift = Mock(
            status="reserved",
            extension_count=0,
            purchase_by=self.now.date() + timedelta(days=2),
        )
        require_extension(gift, self.now.date() + timedelta(days=9), self.now)
        with self.assertRaises(DomainValidationError):
            require_extension(gift, self.now.date() + timedelta(days=10), self.now)
        gift.extension_count = 1
        with self.assertRaises(GiftConflict):
            require_extension(gift, self.now.date() + timedelta(days=4), self.now)

    def test_unchecked_details_are_rejected_for_non_http_callers(self):
        repo = Mock()
        service = GiftingService(
            repo, Mock(), Mock(), Mock(), nullcontext, lambda: self.now
        )
        with self.assertRaises(DomainValidationError):
            service.reserve(
                ReserveGiftInputDTO(
                    wish_id=uuid4(),
                    purchase_by=self.now.date(),
                    purchase_plan="Order online",
                    details_checked=False,
                )
            )
        repo.reserve.assert_not_called()

    def test_giver_cannot_write_recipient_feedback_for_non_http_callers(self):
        repo = Mock()
        service = GiftingService(
            repo, Mock(), Mock(), Mock(), nullcontext, lambda: self.now
        )
        service._authorized_experience = Mock(return_value=(Mock(), False))
        with self.assertRaises(GiftForbidden):
            service.save_experience(
                SaveExperienceInputDTO(
                    reservation_id=1, action="save_private", fit="fits"
                )
            )
        repo.save_experience.assert_not_called()
