from typing import Protocol
from datetime import date, datetime
from uuid import UUID
from src.apps.wishlist.domain import Wish, Wishlist
from src.apps.wishlist.dto import WishOutputDTO, WishlistOutputDTO, ListWishesInputDTO
from src.apps.wishlist.dto.gifting import (
    ActivityOutputDTO,
    GiftRecordOutputDTO,
    GiftOutputDTO,
    InboxOutputDTO,
    ReserveGiftInputDTO,
    SaveExperienceInputDTO,
)
from src.shared.dto import IdInputDTO


class GiftRepository(Protocol):
    def wish(self, id: UUID, *, lock: bool = False) -> Wish | None:
        ...

    def wishlist(self, id: UUID) -> Wishlist | None:
        ...

    def active(self, wish_id: UUID) -> GiftRecordOutputDTO | None:
        ...

    def activities(
        self, wish_ids: tuple[UUID, ...], visitor: str, profile_id: UUID | None
    ) -> tuple[ActivityOutputDTO, ...]:
        ...

    def interact(self, wish_id: UUID, visitor: str, action: str) -> None:
        ...

    def reserve(
        self,
        wish: Wish,
        dto: ReserveGiftInputDTO,
        token_hash: str,
        expires_at: datetime,
        reminder_at: datetime,
        guest_hash: str = "",
    ) -> GiftRecordOutputDTO:
        ...

    def change(self, id: int, status: str, now: datetime) -> GiftRecordOutputDTO:
        ...

    def notify(self, profile_id: UUID, wish: Wish, event: str) -> None:
        ...

    def gifts(self, profile_id: UUID) -> tuple[GiftOutputDTO, ...]:
        ...

    def inbox(self, profile_id: UUID) -> InboxOutputDTO:
        ...

    def read(self, profile_id: UUID, notification_id: UUID | None) -> None:
        ...

    def get_gift(self, id: int) -> GiftRecordOutputDTO | None:
        ...

    def reschedule(
        self, id: int, purchase_by: date, expires_at: datetime, reminder_at: datetime
    ) -> GiftRecordOutputDTO:
        ...

    def candidates(
        self,
        now: datetime,
        *,
        wish_ids: tuple[UUID, ...] | None = None,
        wishlist_id: UUID | None = None,
        reminders: bool = False
    ) -> tuple[UUID, ...]:
        ...

    def mark_reminded(self, id: int, now: datetime) -> None:
        ...

    def save_experience(
        self, dto: SaveExperienceInputDTO, now: datetime
    ) -> GiftRecordOutputDTO:
        ...


class WishlistReader(Protocol):
    def get_wishlist(self, dto: IdInputDTO) -> WishlistOutputDTO | None:
        ...

    def list_wishes(self, dto: ListWishesInputDTO) -> tuple[WishOutputDTO, ...]:
        ...


class GiftCredentials(Protocol):
    def issue(self) -> str:
        ...

    def digest(self, token: str) -> str:
        ...

    def matches(self, token: str, digest: str) -> bool:
        ...


class GiftClock(Protocol):
    def __call__(self) -> datetime:
        ...
