import faker
import uuid
from django.test import TestCase

from src.apps.wishlist.services import update_wish
from src.utils.fakers import WishlistFactory, WishFactory, UserFactory, ProfileFactory
from src.static.serializer_errors import SerializerErrors
from src.utils.exceptions import InvalidWishId, NotWishlistOwner


class UpdateWishTestCase(TestCase):
    def setUp(self):
        self.user_with_profile = UserFactory()
        self.profile = ProfileFactory(profile_id=self.user_with_profile.id)
        self.wishlist = WishlistFactory(profile=self.profile)

        self.wish = WishFactory(
            wishlist=self.wishlist,
            name="Old Laptop",
            description="Gaming laptop",
            price=1200,
        )

    def test_update_wish_successfully(self):
        fake = faker.Faker()
        new_name = fake.word()
        new_description = fake.text()
        new_price = 1500

        updated, data, errs = update_wish(
            self.wish.id,
            {
                "wishlist": self.wishlist.id,
                "name": new_name,
                "description": new_description,
                "price": new_price,
            },
            profile_id=self.profile.profile_id,
        )

        self.assertTrue(updated)
        self.assertIsNone(errs or None)
        self.assertEqual(data.get("name"), new_name)
        self.assertEqual(data.get("description"), new_description)
        self.assertEqual(data.get("price"), str(new_price))

    def test_invalid_update_wish_id_raises(self):
        with self.assertRaises(InvalidWishId):
            update_wish(
                uuid.uuid4(),
                {
                    "wishlist": self.wishlist.id,
                    "description": "Some update",
                },
                profile_id=self.profile.profile_id,
            )

    def test_invalid_update_wish_validation_error(self):
        # Setting description to None (required field)
        updated, data, errs = update_wish(
            self.wish.id,
            {
                "wishlist": self.wishlist.id,
                "description": None,
            },
            profile_id=self.profile.profile_id,
        )

        self.assertFalse(updated)
        self.assertIsNone(data)
        self.assertIn("error_type", errs)

        # Check that the error_type matches SerializerErrors
        error_type = errs.get("error_type")
        self.assertIn(
            SerializerErrors.CreateWishlist.errors.get("description"),
            error_type,
        )

    def test_update_wish_not_owner_raises(self):
        """Ensure a different profile cannot update this wish"""
        another_user = UserFactory()
        another_profile = ProfileFactory(profile_id=another_user.id)

        with self.assertRaises(NotWishlistOwner):
            update_wish(
                self.wish.id,
                {
                    "wishlist": self.wishlist.id,
                    "description": "Trying to update illegally",
                },
                profile_id=another_profile.profile_id,
            )
