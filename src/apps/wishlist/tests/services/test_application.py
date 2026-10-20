from unittest.mock import patch
from uuid import uuid4

from django.test import TestCase

from src.apps.wishlist.domain.errors import NotWishlistOwner, WishNotFound
from src.apps.wishlist.dto import (
    CreateAnonymousFriendInputDTO,
    CreateWishInputDTO,
    CreateWishlistInputDTO,
    ListWishesInputDTO,
    ListWishlistsInputDTO,
    SubmitReservationInputDTO,
    UpdateWishInputDTO,
    UpdateWishlistInputDTO,
    WishActorInputDTO,
    WishlistActorInputDTO,
)
from src.apps.wishlist.models import Wish, Wishlist
from src.core.composition import wishlist_service
from src.shared.domain.errors import DomainValidationError
from src.shared.dto import IdInputDTO
from src.utils.fakers import ProfileFactory, WishFactory, WishlistFactory


class WishlistServiceIntegrationTests(TestCase):
    def setUp(self):
        self.profile = ProfileFactory()
        self.wishlist = WishlistFactory(profile=self.profile)
        self.wish = WishFactory(wishlist=self.wishlist)
        self.service = wishlist_service()

    def test_create_read_and_list_wishlist(self):
        output = self.service.create_wishlist(
            CreateWishlistInputDTO(
                profile_id=self.profile.profile_id, name="Books", description="Novels"
            )
        )
        self.assertEqual(self.service.get_wishlist(IdInputDTO(id=output.id)), output)
        self.assertEqual(
            len(
                self.service.list_wishlists(
                    ListWishlistsInputDTO(profile_id=self.profile.profile_id)
                )
            ),
            2,
        )

    def test_create_wish_and_update_partial_fields(self):
        output = self.service.create_wish(
            CreateWishInputDTO(
                wishlist_id=self.wishlist.id,
                profile_id=self.profile.profile_id,
                name="Book",
                description="Novel",
                price=100,
            )
        )
        result = self.service.update_wish(
            UpdateWishInputDTO(
                id=output.id,
                wishlist_id=self.wishlist.id,
                profile_id=self.profile.profile_id,
                name="New",
            )
        )
        self.assertEqual(result.name, "New")
        self.assertEqual(result.description, "Novel")
        self.assertEqual(result.price, 100)

    def test_partial_update_preserves_cover_and_explicit_null_clears_it(self):
        from src.utils.fakers import MediaModelFactory

        media = MediaModelFactory()
        self.wishlist.cover = media
        self.wishlist.save()
        result = self.service.update_wishlist(
            UpdateWishlistInputDTO(
                id=self.wishlist.id, profile_id=self.profile.profile_id, name="New"
            )
        )
        self.assertIsNotNone(result.cover)
        result = self.service.update_wishlist(
            UpdateWishlistInputDTO(
                id=self.wishlist.id, profile_id=self.profile.profile_id, cover_id=None
            )
        )
        self.assertIsNone(result.cover)

    def test_ownership_is_enforced_without_view_permissions(self):
        with self.assertRaises(NotWishlistOwner):
            self.service.update_wish(
                UpdateWishInputDTO(
                    id=self.wish.id,
                    wishlist_id=self.wishlist.id,
                    profile_id=uuid4(),
                    name="Hijack",
                )
            )
        self.wish.refresh_from_db()
        self.assertNotEqual(self.wish.name, "Hijack")

    def test_wish_cannot_be_deleted_through_a_different_owned_wishlist(self):
        other = WishlistFactory(profile=self.profile)
        with self.assertRaises(WishNotFound):
            self.service.delete_wish(
                WishActorInputDTO(
                    id=self.wish.id,
                    wishlist_id=other.id,
                    profile_id=self.profile.profile_id,
                )
            )
        self.assertTrue(Wish.objects.filter(id=self.wish.id).exists())

    def test_delete_wish_and_wishlist(self):
        self.assertTrue(
            self.service.delete_wish(
                WishActorInputDTO(
                    id=self.wish.id,
                    wishlist_id=self.wishlist.id,
                    profile_id=self.profile.profile_id,
                )
            ).deleted
        )
        self.assertTrue(
            self.service.delete_wishlist(
                WishlistActorInputDTO(
                    id=self.wishlist.id, profile_id=self.profile.profile_id
                )
            ).deleted
        )
        self.assertFalse(Wishlist.objects.filter(id=self.wishlist.id).exists())

    def test_registered_and_anonymous_reservations(self):
        friend = self.service.create_anonymous_friend(
            CreateAnonymousFriendInputDTO(nickname="Friend")
        )
        for fields in (
            {"friend_id": self.profile.profile_id},
            {"anonymous_friend_id": friend.id},
        ):
            output = self.service.submit_reservation(
                SubmitReservationInputDTO(wish_id=self.wish.id, **fields)
            )
            self.assertEqual(output.status, "pending")
            self.assertEqual(output.wish, self.wish.id)

    def test_unknown_cover_is_business_validation(self):
        with self.assertRaises(DomainValidationError):
            self.service.update_wishlist(
                UpdateWishlistInputDTO(
                    id=self.wishlist.id,
                    profile_id=self.profile.profile_id,
                    cover_id=uuid4(),
                )
            )

    def test_write_failure_rolls_back_persistence(self):
        original = self.service.repository.create_wish

        def fail_after_create(dto):
            original(dto)
            raise RuntimeError("Persistence failure")

        count = Wish.objects.count()
        with patch.object(
            self.service.repository, "create_wish", side_effect=fail_after_create
        ):
            with self.assertRaises(RuntimeError):
                self.service.create_wish(
                    CreateWishInputDTO(
                        wishlist_id=self.wishlist.id,
                        profile_id=self.profile.profile_id,
                        name="Book",
                        description="Novel",
                        price=100,
                    )
                )
        self.assertEqual(Wish.objects.count(), count)

    def test_list_cover_lookup_is_batched(self):
        from src.utils.fakers import MediaModelFactory

        media = MediaModelFactory()
        WishFactory.create_batch(3, wishlist=self.wishlist, cover=media)
        with self.assertNumQueries(2):
            self.service.list_wishes(ListWishesInputDTO(wishlist_id=self.wishlist.id))
