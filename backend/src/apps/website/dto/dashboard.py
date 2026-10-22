"""Snapshots shared through the dashboard's consumer-owned contracts."""

from datetime import date, datetime

from src.shared.dto import DTO


class UserMetricsDTO(DTO):
    total: int
    enabled: int
    active: int
    new: int


class GenderWishCountsDTO(DTO):
    gender: str
    total: int
    fulfilled: int


class DailyWishCountsDTO(DTO):
    day: date
    created: int = 0
    fulfilled: int = 0


class WishMetricsDTO(DTO):
    total: int
    fulfilled: int
    reserved: int
    purchased: int
    recent: int
    by_gender: tuple[GenderWishCountsDTO, ...]
    daily: tuple[DailyWishCountsDTO, ...]


class GenderFulfillmentDTO(GenderWishCountsDTO):
    label: str
    rate: float | None


class DashboardOutputDTO(DTO):
    generated_at: datetime
    active_since: datetime
    chart_since: date
    users: UserMetricsDTO
    wishes: WishMetricsDTO
    fulfillment_rate: float | None
    awaiting: int
    by_gender: tuple[GenderFulfillmentDTO, ...]
    daily: tuple[DailyWishCountsDTO, ...]
