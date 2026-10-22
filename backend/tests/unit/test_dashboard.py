from datetime import datetime, timedelta, timezone
from unittest import TestCase
from unittest.mock import Mock

from src.apps.website.dto.dashboard import (
    DailyWishCountsDTO,
    GenderWishCountsDTO,
    UserMetricsDTO,
    WishMetricsDTO,
)
from src.apps.website.interfaces import UserMetricsReader, WishMetricsReader
from src.apps.website.services.dashboard import DashboardService


class DashboardTests(TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 22, 12, tzinfo=timezone.utc)
        self.users = Mock(spec=UserMetricsReader)
        self.wishes = Mock(spec=WishMetricsReader)
        self.users.read.return_value = UserMetricsDTO(
            total=10, enabled=8, active=4, new=2
        )
        self.wishes.read.return_value = WishMetricsDTO(
            total=10,
            fulfilled=3,
            reserved=2,
            purchased=1,
            recent=4,
            by_gender=(
                GenderWishCountsDTO(gender="female", total=2, fulfilled=1),
                GenderWishCountsDTO(gender="male", total=8, fulfilled=2),
            ),
            daily=(DailyWishCountsDTO(day=self.now.date(), created=4, fulfilled=1),),
        )
        self.service = DashboardService(self.users, self.wishes, lambda: self.now)

    def test_rates_are_per_wish_and_unknown_gender_is_explicit(self):
        result = self.service.overview()
        self.assertEqual(result.fulfillment_rate, 30.0)
        self.assertEqual(result.awaiting, 4)
        self.assertEqual([group.rate for group in result.by_gender], [50.0, 25.0, None])
        self.assertEqual(result.by_gender[-1].label, "Not specified")

    def test_rolling_activity_and_calendar_chart_have_distinct_cutoffs(self):
        result = self.service.overview()
        self.users.read.assert_called_once_with(self.now - timedelta(days=30), self.now)
        start = (self.now - timedelta(days=29)).replace(hour=0)
        self.wishes.read.assert_called_once_with(start, self.now)
        self.assertEqual(len(result.daily), 30)
        self.assertEqual(result.daily[0].day, start.date())
        self.assertEqual(result.daily[0].created, 0)
        self.assertEqual(result.daily[-1].created, 4)

    def test_no_wishes_has_no_rate_instead_of_division_by_zero(self):
        self.wishes.read.return_value = WishMetricsDTO(
            total=0,
            fulfilled=0,
            reserved=0,
            purchased=0,
            recent=0,
            by_gender=(),
            daily=(),
        )
        result = self.service.overview()
        self.assertIsNone(result.fulfillment_rate)
        self.assertEqual(result.awaiting, 0)
        self.assertTrue(all(group.rate is None for group in result.by_gender))
