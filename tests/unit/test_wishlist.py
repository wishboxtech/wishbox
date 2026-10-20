from contextlib import contextmanager
from dataclasses import replace
from datetime import datetime, timezone
from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock
from uuid import uuid4

from pydantic import ValidationError

from src.apps.storage.interfaces import StorageServiceProtocol
from src.apps.wishlist.domain import Wish, Wishlist
from src.apps.wishlist.domain.errors import NotWishlistOwner, WishNotFound
from src.apps.wishlist.dto import (
    CreateWishInputDTO,
    CreateWishlistInputDTO,
    ListWishesInputDTO,
    SubmitReservationInputDTO,
    UpdateWishInputDTO,
    UpdateWishlistInputDTO,
    WishActorInputDTO,
    WishlistActorInputDTO,
)
from src.apps.wishlist.interfaces import ProfileServiceProtocol, WishlistRepository
from src.apps.wishlist.services import WishlistService
from src.shared.domain.errors import DomainValidationError


class WishlistUnitTests(TestCase):
    def setUp(self):
        self.owner = uuid4()
        now = datetime.now(timezone.utc)
        self.wishlist = Wishlist(
            uuid4(), self.owner, "Birthday", "Books", None, now, now
        )
        self.wish = Wish(
            uuid4(),
            self.wishlist.id,
            "Book",
            "Novel",
            Decimal(100),
            None,
            None,
            now,
            now,
        )
        self.repo = Mock(spec=WishlistRepository)
        self.profile = Mock(spec=ProfileServiceProtocol)
        self.storage = Mock(spec=StorageServiceProtocol)
        self.events = []

        @contextmanager
        def transaction():
            self.events.append("enter")
            try:
                yield
            except Exception:
                self.events.append("rollback")
                raise
            else:
                self.events.append("commit")

        self.service = WishlistService(
            self.repo, self.profile, self.storage, transaction
        )
        self.repo.get_wishlist.return_value = self.wishlist
        self.repo.get_wish.return_value = self.wish

    def test_create_wish_runs_owner_policy_inside_transaction(self):
        self.repo.create_wish.return_value = self.wish
        dto = CreateWishInputDTO(
            wishlist_id=self.wishlist.id,
            profile_id=self.owner,
            name="Book",
            description="Novel",
            price=100,
        )
        output = self.service.create_wish(dto)
        self.assertEqual(output.id, self.wish.id)
        self.assertEqual(self.events, ["enter", "commit"])
        self.repo.get_wishlist.assert_called_once_with(self.wishlist.id, lock=True)

    def test_non_owner_cannot_create_wish(self):
        dto = CreateWishInputDTO(
            wishlist_id=self.wishlist.id,
            profile_id=uuid4(),
            name="Book",
            description="Novel",
            price=100,
        )
        with self.assertRaises(NotWishlistOwner):
            self.service.create_wish(dto)
        self.repo.create_wish.assert_not_called()
        self.assertEqual(self.events, ["enter", "rollback"])

    def test_update_without_destination_still_requires_current_owner(self):
        dto = UpdateWishInputDTO(
            id=self.wish.id,
            wishlist_id=self.wishlist.id,
            profile_id=uuid4(),
            description="New",
        )
        with self.assertRaises(NotWishlistOwner):
            self.service.update_wish(dto)
        self.repo.update_wish.assert_not_called()

    def test_cannot_update_wish_using_another_owned_wishlist(self):
        self.repo.get_wish.return_value = replace(self.wish, wishlist_id=uuid4())
        dto = UpdateWishInputDTO(
            id=self.wish.id,
            wishlist_id=self.wishlist.id,
            profile_id=self.owner,
            description="New",
        )
        with self.assertRaises(WishNotFound):
            self.service.update_wish(dto)
        self.repo.update_wish.assert_not_called()

    def test_cannot_delete_wish_using_another_owned_wishlist(self):
        self.repo.get_wish.return_value = replace(self.wish, wishlist_id=uuid4())
        dto = WishActorInputDTO(
            id=self.wish.id, wishlist_id=self.wishlist.id, profile_id=self.owner
        )
        with self.assertRaises(WishNotFound):
            self.service.delete_wish(dto)
        self.repo.delete_wish.assert_not_called()

    def test_update_wishlist_always_checks_actor(self):
        with self.assertRaises(NotWishlistOwner):
            self.service.update_wishlist(
                UpdateWishlistInputDTO(
                    id=self.wishlist.id, profile_id=uuid4(), name="New"
                )
            )
        self.repo.update_wishlist.assert_not_called()

    def test_delete_wishlist_always_checks_actor(self):
        with self.assertRaises(NotWishlistOwner):
            self.service.delete_wishlist(
                WishlistActorInputDTO(id=self.wishlist.id, profile_id=uuid4())
            )
        self.repo.delete_wishlist.assert_not_called()

    def test_missing_wish_delete_is_explicit_false(self):
        self.repo.get_wish.return_value = None
        output = self.service.delete_wish(
            WishActorInputDTO(
                id=uuid4(), wishlist_id=self.wishlist.id, profile_id=self.owner
            )
        )
        self.assertFalse(output.deleted)

    def test_create_wishlist_requires_existing_profile(self):
        self.profile.exists.return_value = False
        with self.assertRaises(DomainValidationError):
            self.service.create_wishlist(
                CreateWishlistInputDTO(
                    profile_id=self.owner, name="Birthday", description="Books"
                )
            )
        self.repo.create_wishlist.assert_not_called()

    def test_reservation_requires_actor_even_without_http(self):
        with self.assertRaises(DomainValidationError) as context:
            self.service.submit_reservation(
                SubmitReservationInputDTO(wish_id=self.wish.id)
            )
        self.assertEqual(set(context.exception.errors), {"friend", "anonymous_friend"})
        self.repo.create_reservation.assert_not_called()

    def test_reservation_rejects_missing_wish(self):
        self.repo.get_wish.return_value = None
        with self.assertRaises(DomainValidationError):
            self.service.submit_reservation(
                SubmitReservationInputDTO(wish_id=uuid4(), friend_id=self.owner)
            )

    def test_reservation_rejects_unknown_anonymous_friend(self):
        self.repo.anonymous_friend_exists.return_value = False
        with self.assertRaises(DomainValidationError):
            self.service.submit_reservation(
                SubmitReservationInputDTO(
                    wish_id=self.wish.id, anonymous_friend_id=uuid4()
                )
            )

    def test_partial_update_distinguishes_omission_from_null(self):
        dto = UpdateWishInputDTO(
            id=self.wish.id,
            wishlist_id=self.wishlist.id,
            profile_id=self.owner,
            cover_id=None,
        )
        self.assertEqual(
            dto.model_dump(
                exclude_unset=True, exclude={"id", "wishlist_id", "profile_id"}
            ),
            {"cover_id": None},
        )
        with self.assertRaises(ValidationError):
            UpdateWishInputDTO(
                id=self.wish.id,
                wishlist_id=self.wishlist.id,
                profile_id=self.owner,
                description=None,
            )

    def test_dto_rejects_framework_objects_unknown_fields_and_mutation(self):
        dto = WishlistActorInputDTO(id=self.wishlist.id, profile_id=self.owner)
        with self.assertRaises(ValidationError):
            dto.id = uuid4()
        with self.assertRaises(ValidationError):
            WishlistActorInputDTO(
                id=self.wishlist.id, profile_id=self.owner, request=object()
            )

    def test_list_uses_one_media_batch(self):
        cover_id = uuid4()
        self.repo.list_wishes.return_value = (
            replace(self.wish, cover_id=cover_id),
            self.wish,
        )
        self.storage.get_media_batch.return_value = {}
        self.assertEqual(
            len(
                self.service.list_wishes(
                    ListWishesInputDTO(wishlist_id=self.wishlist.id)
                )
            ),
            2,
        )
        self.storage.get_media_batch.assert_called_once_with((cover_id,))
        self.storage.get_media.assert_not_called()
