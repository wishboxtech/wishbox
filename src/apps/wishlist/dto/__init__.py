from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import Field, StringConstraints, field_validator

from src.apps.storage.dto import MediaOutputDTO
from src.shared.dto import DTO

Name = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)
]
Price = Annotated[Decimal, Field(max_digits=10, decimal_places=0)]


class CreateWishlistInputDTO(DTO):
    profile_id: UUID
    name: Name
    description: str
    cover_id: UUID | None = None


class UpdateWishlistInputDTO(DTO):
    id: UUID
    profile_id: UUID
    name: Name | None = None
    description: str | None = None
    cover_id: UUID | None = None

    @field_validator("name", "description")
    @classmethod
    def non_nullable_fields(cls, value):
        if value is None:
            raise ValueError("This field cannot be null.")
        return value


class WishlistOutputDTO(DTO):
    id: UUID
    name: str
    description: str
    cover: MediaOutputDTO | None
    created_at: datetime
    updated_at: datetime


class ListWishlistsInputDTO(DTO):
    profile_id: UUID


class WishlistActorInputDTO(DTO):
    id: UUID
    profile_id: UUID


class CreateWishInputDTO(DTO):
    wishlist_id: UUID
    profile_id: UUID
    name: Name
    description: str
    price: Price
    cover_id: UUID | None = None


class UpdateWishInputDTO(DTO):
    id: UUID
    wishlist_id: UUID
    profile_id: UUID
    name: Name | None = None
    description: str | None = None
    price: Price | None = None
    cover_id: UUID | None = None

    @field_validator("name", "description", "price")
    @classmethod
    def non_nullable_fields(cls, value):
        if value is None:
            raise ValueError("This field cannot be null.")
        return value


class WishOutputDTO(DTO):
    id: UUID
    name: str
    description: str
    price: Decimal
    cover: MediaOutputDTO | None
    created_at: datetime
    updated_at: datetime


class ListWishesInputDTO(DTO):
    wishlist_id: UUID


class WishActorInputDTO(DTO):
    id: UUID
    wishlist_id: UUID
    profile_id: UUID


class CreateAnonymousFriendInputDTO(DTO):
    nickname: Name

    @field_validator("nickname")
    @classmethod
    def nickname_is_not_blank(cls, value):
        if not value.strip():
            raise ValueError("Nickname cannot be blank.")
        return value


class AnonymousFriendOutputDTO(DTO):
    id: UUID


class SubmitReservationInputDTO(DTO):
    wish_id: UUID
    friend_id: UUID | None = None
    anonymous_friend_id: UUID | None = None


class ReservationOutputDTO(DTO):
    wish: UUID
    friend: UUID | None
    anonymous_friend: UUID | None
    status: str
    created_at: datetime
