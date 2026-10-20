from typing import Mapping
from uuid import UUID

from src.apps.storage.dto import MediaOutputDTO
from src.apps.storage.interfaces import StorageServiceProtocol
from src.apps.wishlist.domain import Wish, Wishlist
from src.apps.wishlist.domain.errors import WishlistNotFound, WishNotFound
from src.apps.wishlist.domain.policies import require_reservation_actor
from src.apps.wishlist.dto import (
    AnonymousFriendOutputDTO,
    CreateAnonymousFriendInputDTO,
    CreateWishInputDTO,
    CreateWishlistInputDTO,
    ListWishesInputDTO,
    ListWishlistsInputDTO,
    ReservationOutputDTO,
    SubmitReservationInputDTO,
    UpdateWishInputDTO,
    UpdateWishlistInputDTO,
    WishActorInputDTO,
    WishlistActorInputDTO,
    WishlistOutputDTO,
    WishOutputDTO,
)
from src.apps.wishlist.interfaces import ProfileServiceProtocol, WishlistRepository
from src.shared.domain.errors import DomainValidationError
from src.shared.dto import DeleteOutputDTO, IdInputDTO
from src.shared.interfaces import TransactionBoundary


class WishlistService:
    def __init__(
        self,
        repository: WishlistRepository,
        profile: ProfileServiceProtocol,
        storage: StorageServiceProtocol,
        transaction: TransactionBoundary,
    ):
        self.repository = repository
        self.profile = profile
        self.storage = storage
        self.transaction = transaction

    def _cover_output(
        self, cover_id: UUID | None, covers: Mapping[UUID, MediaOutputDTO] | None
    ):
        if cover_id is None:
            return None
        if covers is None:
            return self.storage.get_media(cover_id)
        return covers.get(cover_id)

    def _wishlist_output(self, wishlist: Wishlist, covers=None) -> WishlistOutputDTO:
        return WishlistOutputDTO(
            id=wishlist.id,
            name=wishlist.name,
            description=wishlist.description,
            cover=self._cover_output(wishlist.cover_id, covers),
            created_at=wishlist.created_at,
            updated_at=wishlist.updated_at,
        )

    def _wish_output(self, wish: Wish, covers=None) -> WishOutputDTO:
        return WishOutputDTO(
            wishlist_id=wish.wishlist_id,
            id=wish.id,
            name=wish.name,
            description=wish.description,
            price=wish.price,
            cover=self._cover_output(wish.cover_id, covers),
            created_at=wish.created_at,
            updated_at=wish.updated_at,
        )

    def _owned_wishlist(self, id: UUID, profile_id: UUID) -> Wishlist:
        wishlist = self.repository.get_wishlist(id, lock=True)
        if wishlist is None:
            raise WishlistNotFound()
        wishlist.require_owner(profile_id)
        return wishlist

    def _check_cover(self, cover_id):
        if cover_id is not None and self.storage.get_media(cover_id) is None:
            raise DomainValidationError({"cover": "Media does not exist."})

    def list_wishlists(
        self, dto: ListWishlistsInputDTO
    ) -> tuple[WishlistOutputDTO, ...]:
        items = self.repository.list_wishlists(dto.profile_id)
        covers = self.storage.get_media_batch(
            tuple(item.cover_id for item in items if item.cover_id)
        )
        return tuple(self._wishlist_output(item, covers) for item in items)

    def get_wishlist(self, dto: IdInputDTO) -> WishlistOutputDTO | None:
        item = self.repository.get_wishlist(dto.id)
        return self._wishlist_output(item) if item else None

    def create_wishlist(self, dto: CreateWishlistInputDTO) -> WishlistOutputDTO:
        with self.transaction():
            if not self.profile.exists(dto.profile_id):
                raise DomainValidationError({"profile": "Profile does not exist."})
            self._check_cover(dto.cover_id)
            item = self.repository.create_wishlist(dto)
        return self._wishlist_output(item)

    def update_wishlist(self, dto: UpdateWishlistInputDTO) -> WishlistOutputDTO:
        with self.transaction():
            self._owned_wishlist(dto.id, dto.profile_id)
            self._check_cover(dto.cover_id)
            item = self.repository.update_wishlist(dto)
        return self._wishlist_output(item)

    def delete_wishlist(self, dto: WishlistActorInputDTO) -> DeleteOutputDTO:
        with self.transaction():
            item = self.repository.get_wishlist(dto.id, lock=True)
            if item is None:
                return DeleteOutputDTO(deleted=False)
            item.require_owner(dto.profile_id)
            deleted = self.repository.delete_wishlist(dto.id)
        return DeleteOutputDTO(deleted=deleted)

    def list_wishes(self, dto: ListWishesInputDTO) -> tuple[WishOutputDTO, ...]:
        items = self.repository.list_wishes(dto.wishlist_id)
        covers = self.storage.get_media_batch(
            tuple(item.cover_id for item in items if item.cover_id)
        )
        return tuple(self._wish_output(item, covers) for item in items)

    def get_wish(self, dto: IdInputDTO) -> WishOutputDTO | None:
        item = self.repository.get_wish(dto.id)
        return self._wish_output(item) if item else None

    def create_wish(self, dto: CreateWishInputDTO) -> WishOutputDTO:
        with self.transaction():
            self._owned_wishlist(dto.wishlist_id, dto.profile_id)
            self._check_cover(dto.cover_id)
            item = self.repository.create_wish(dto)
        return self._wish_output(item)

    def update_wish(self, dto: UpdateWishInputDTO) -> WishOutputDTO:
        with self.transaction():
            self._owned_wishlist(dto.wishlist_id, dto.profile_id)
            item = self.repository.get_wish(dto.id, lock=True)
            if item is None:
                raise WishNotFound()
            item.require_wishlist(dto.wishlist_id)
            self._check_cover(dto.cover_id)
            item = self.repository.update_wish(dto)
        return self._wish_output(item)

    def delete_wish(self, dto: WishActorInputDTO) -> DeleteOutputDTO:
        with self.transaction():
            self._owned_wishlist(dto.wishlist_id, dto.profile_id)
            item = self.repository.get_wish(dto.id, lock=True)
            if item is None:
                return DeleteOutputDTO(deleted=False)
            item.require_wishlist(dto.wishlist_id)
            deleted = self.repository.delete_wish(dto.id)
        return DeleteOutputDTO(deleted=deleted)

    def create_anonymous_friend(
        self, dto: CreateAnonymousFriendInputDTO
    ) -> AnonymousFriendOutputDTO:
        with self.transaction():
            return self.repository.create_anonymous_friend(dto)

    def submit_reservation(
        self, dto: SubmitReservationInputDTO
    ) -> ReservationOutputDTO:
        require_reservation_actor(dto.friend_id, dto.anonymous_friend_id)
        raise DomainValidationError(
            {
                "reservation": "Use GiftingService.reserve with a verified actor or a guest nickname."
            }
        )
