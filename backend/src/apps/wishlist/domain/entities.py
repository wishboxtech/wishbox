from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from src.apps.wishlist.domain.errors import NotWishlistOwner, WishNotFound


@dataclass(frozen=True)
class Wishlist:
    id: UUID
    profile_id: UUID
    name: str
    description: str
    cover_id: UUID | None
    created_at: datetime
    updated_at: datetime

    def require_owner(self, profile_id: UUID) -> None:
        if self.profile_id != profile_id:
            raise NotWishlistOwner()


@dataclass(frozen=True)
class Wish:
    id: UUID
    wishlist_id: UUID
    name: str
    description: str
    price: Decimal
    cover_id: UUID | None
    accepted_request_id: int | None
    created_at: datetime
    updated_at: datetime

    def require_wishlist(self, wishlist_id: UUID) -> None:
        if self.wishlist_id != wishlist_id:
            raise WishNotFound()
