"""Combine administrative snapshots without framework or database dependencies."""

from collections.abc import Callable
from datetime import datetime, timedelta, timezone

from src.apps.website.dto.dashboard import (
    DailyWishCountsDTO,
    DashboardOutputDTO,
    GenderFulfillmentDTO,
)
from src.apps.website.interfaces import UserMetricsReader, WishMetricsReader


def fulfillment_rate(fulfilled: int, total: int) -> float | None:
    return round(100 * fulfilled / total, 1) if total else None


class DashboardService:
    def __init__(
        self,
        users: UserMetricsReader,
        wishes: WishMetricsReader,
        clock: Callable[[], datetime],
    ):
        self.users = users
        self.wishes = wishes
        self.clock = clock

    def overview(self) -> DashboardOutputDTO:
        now = self.clock().astimezone(timezone.utc)
        active_since = now - timedelta(days=30)
        chart_since = (now - timedelta(days=29)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        users = self.users.read(active_since, now)
        wishes = self.wishes.read(chart_since, now)
        counts = {item.gender: item for item in wishes.by_gender}
        groups = []
        for gender, label in (
            ("female", "Female"),
            ("male", "Male"),
            ("unknown", "Not specified"),
        ):
            group = counts.get(gender)
            total = group.total if group else 0
            fulfilled = group.fulfilled if group else 0
            groups.append(
                GenderFulfillmentDTO(
                    gender=gender,
                    label=label,
                    total=total,
                    fulfilled=fulfilled,
                    rate=fulfillment_rate(fulfilled, total),
                )
            )
        daily = {item.day: item for item in wishes.daily}
        return DashboardOutputDTO(
            generated_at=now,
            active_since=active_since,
            chart_since=chart_since.date(),
            users=users,
            wishes=wishes,
            fulfillment_rate=fulfillment_rate(wishes.fulfilled, wishes.total),
            awaiting=wishes.total
            - wishes.fulfilled
            - wishes.reserved
            - wishes.purchased,
            by_gender=tuple(groups),
            daily=tuple(
                daily.get(day, DailyWishCountsDTO(day=day))
                for day in (
                    chart_since.date() + timedelta(days=offset) for offset in range(30)
                )
            ),
        )
