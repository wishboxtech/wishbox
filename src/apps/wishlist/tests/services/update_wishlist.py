import uuid

import faker
from django.test import TestCase

from src.apps.wishlist.services import update_wishlist
from src.static.serializer_errors import SerializerErrors
from src.utils.exceptions import InvalidWishlistId
from src.utils.fakers import ProfileFactory, UserFactory, WishlistFactory


class UpdateWishlistTestCase(TestCase):
    def setUp(self):
        self.user_with_profile = UserFactory()
        self.profile = ProfileFactory(profile_id=self.user_with_profile.id)
        self.wishlist = WishlistFactory(
            profile=self.profile,
            name="Birthday",
            description="Valuable wishlist",
        )

    def test_create_wishlist(self):
        wishlist_name = faker.Faker().name()
        wishlist_description = faker.Faker().text()

        updated, data, _ = update_wishlist(
            self.wishlist.id,
            {
                "profile": self.profile.profile_id,
                "name": wishlist_name,
                "description": wishlist_description,
            },
        )
        self.assertTrue(updated)
        self.assertEqual(data.get("name"), wishlist_name)
        self.assertEqual(data.get("description"), wishlist_description)

    def test_invalid_update_wishlist(self):

        with self.assertRaises(InvalidWishlistId):
            update_wishlist(
                uuid.uuid4(),
                {
                    "profile": self.profile.profile_id,
                    "description": None,
                },
            )

        updated, _, errs = update_wishlist(
            self.wishlist.id,
            {
                "profile": self.profile.profile_id,
                "description": None,
            },
        )

        self.assertFalse(updated)

        error_type = errs.get("error_type")
        self.assertEqual(
            error_type, [SerializerErrors.CreateWishlist.errors.get("description")]
        )
