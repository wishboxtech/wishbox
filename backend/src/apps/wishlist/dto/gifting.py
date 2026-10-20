from datetime import date, datetime
from typing import Annotated, Literal
from uuid import UUID
from pydantic import Field, StringConstraints
from src.shared.dto import DTO
from src.apps.wishlist.dto import Name, WishlistOutputDTO, WishOutputDTO


class ActivityInputDTO(DTO):
    wish_id: UUID
    visitor: UUID
    profile_id: UUID | None = None
    action: Literal["view", "like", "unlike"] | None = None
    token: str = Field(default="", max_length=200)


class ReserveGiftInputDTO(DTO):
    wish_id: UUID
    profile_id: UUID | None = None
    nickname: Name = "A friend"
    guest_key: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")] | None = None
    purchase_by: date
    purchase_plan: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=3, max_length=160)
    ]
    details_checked: bool


class ChangeGiftInputDTO(DTO):
    purchase_by: date | None = None
    wish_id: UUID
    action: Literal["purchase", "cancel", "receive", "reschedule"]
    profile_id: UUID | None = None
    token: str = Field(default="", max_length=200)


class GiftRecordOutputDTO(DTO):
    id: int
    wish_id: UUID
    wishlist_id: UUID
    owner_id: UUID
    friend_id: UUID | None
    management_hash: str
    purchase_by: date | None = None
    purchase_plan: str = ""
    details_checked: bool = False
    expires_at: datetime | None = None
    reminder_at: datetime | None = None
    reminded_at: datetime | None = None
    extension_count: int = 0
    received_at: datetime | None = None
    fit: str = ""
    private_note: str = ""
    thank_you: str = ""
    thank_you_sent_at: datetime | None = None
    follow_up_note: str = ""
    follow_up_sent_at: datetime | None = None
    follow_up_acknowledged_at: datetime | None = None
    status: str
    wish_name: str
    created_at: datetime


class GiftOutputDTO(DTO):
    id: int
    wish_id: UUID
    wishlist_id: UUID
    wish_name: str
    status: str
    created_at: datetime
    management_token: str | None = None
    purchase_by: date | None = None
    purchase_plan: str = ""
    expires_at: datetime | None = None
    extension_count: int = 0
    received_at: datetime | None = None
    thank_you: str = ""
    thank_you_sent_at: datetime | None = None
    follow_up_note: str = ""
    follow_up_sent_at: datetime | None = None
    follow_up_acknowledged_at: datetime | None = None


class ActivityOutputDTO(DTO):
    wish_id: UUID
    views: int
    likes: int
    liked: bool
    status: str
    is_owner: bool
    is_giver: bool
    reservation_id: int | None = None


class SharedListInputDTO(DTO):
    wishlist_id: UUID
    visitor: UUID
    profile_id: UUID | None = None


class SharedListOutputDTO(DTO):
    wishlist: WishlistOutputDTO
    wishes: tuple[WishOutputDTO, ...]
    activity: tuple[ActivityOutputDTO, ...]
    is_owner: bool


class NotificationOutputDTO(DTO):
    id: UUID
    wish_id: UUID | None
    wish_name: str
    event: str
    read_at: datetime | None
    created_at: datetime


class InboxOutputDTO(DTO):
    items: tuple[NotificationOutputDTO, ...]
    unread: int


class InboxInputDTO(DTO):
    profile_id: UUID
    notification_id: UUID | None = None


class GiftExperienceInputDTO(DTO):
    reservation_id: int
    profile_id: UUID | None = None
    token: str = Field(default="", max_length=200)


class SaveExperienceInputDTO(GiftExperienceInputDTO):
    follow_up_note: Annotated[
        str, StringConstraints(strip_whitespace=True, max_length=800)
    ] = ""
    action: Literal[
        "save_private",
        "share_thanks",
        "withdraw_thanks",
        "share_follow_up",
        "withdraw_follow_up",
        "acknowledge_follow_up",
    ]
    fit: Literal["fits", "adjust", "not_for_me", "trying"] | None = None
    private_note: Annotated[
        str, StringConstraints(strip_whitespace=True, max_length=800)
    ] = ""
    thank_you: Annotated[
        str, StringConstraints(strip_whitespace=True, max_length=800)
    ] = ""


class OwnerGiftSummaryOutputDTO(DTO):
    id: int
    wish_id: UUID
    wish_name: str
    status: str
    received_at: datetime | None


class OwnerExperienceOutputDTO(DTO):
    role: Literal["owner"] = "owner"
    gift: OwnerGiftSummaryOutputDTO
    fit: str
    private_note: str
    thank_you: str
    thank_you_sent_at: datetime | None
    follow_up_note: str
    follow_up_sent_at: datetime | None
    follow_up_acknowledged_at: datetime | None


class GiverExperienceOutputDTO(DTO):
    role: Literal["giver"] = "giver"
    gift: GiftOutputDTO


class MaintenanceOutputDTO(DTO):
    expired: int
    reminded: int
