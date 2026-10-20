from typing import Protocol
from uuid import UUID

from src.apps.wishlist.domain import Wish, Wishlist
from src.apps.wishlist.dto import (
    AnonymousFriendOutputDTO,
    CreateAnonymousFriendInputDTO,
    CreateWishInputDTO,
    CreateWishlistInputDTO,
    ReservationOutputDTO,
    SubmitReservationInputDTO,
    UpdateWishInputDTO,
    UpdateWishlistInputDTO,
)


class WishlistRepository(Protocol):
    def get_wishlist(self, id: UUID, *, lock: bool = False) -> Wishlist | None:
        ...

    def list_wishlists(self, profile_id: UUID) -> tuple[Wishlist, ...]:
        ...

    def create_wishlist(self, dto: CreateWishlistInputDTO) -> Wishlist:
        ...

    def update_wishlist(self, dto: UpdateWishlistInputDTO) -> Wishlist:
        ...

    def delete_wishlist(self, id: UUID) -> bool:
        ...

    def get_wish(self, id: UUID, *, lock: bool = False) -> Wish | None:
        ...

    def list_wishes(self, wishlist_id: UUID) -> tuple[Wish, ...]:
        ...

    def create_wish(self, dto: CreateWishInputDTO) -> Wish:
        ...

    def update_wish(self, dto: UpdateWishInputDTO) -> Wish:
        ...

    def delete_wish(self, id: UUID) -> bool:
        ...

    def create_anonymous_friend(
        self, dto: CreateAnonymousFriendInputDTO
    ) -> AnonymousFriendOutputDTO:
        ...

    def anonymous_friend_exists(self, id: UUID) -> bool:
        ...

    def create_reservation(
        self, dto: SubmitReservationInputDTO
    ) -> ReservationOutputDTO:
        ...


class ProfileServiceProtocol(Protocol):
    """ProfileService capabilities required by WishlistService."""

    def exists(self, id: UUID) -> bool:
        ...
