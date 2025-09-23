import faker

from django.test import TestCase

from src.apps.wishlist.services import create_wishlist
from src.utils.fakers import WishlistFactory, UserFactory, ProfileFactory
from src.static.serializer_errors import SerializerErrors


class CreateWishlistTestCase(TestCase):
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

        created, data, _ = create_wishlist(
            {
                "profile": self.profile.profile_id,
                "name": wishlist_name,
                "description": wishlist_description,
            },
        )
        self.assertTrue(created)

        self.assertEqual(data.get("name"), wishlist_name)
        self.assertEqual(data.get("description"), wishlist_description)

    def test_invalid_create_wishlist(self):

        created, _, errs = create_wishlist(
            {
                "profile": self.profile.profile_id,
                "description": None,
            },
        )
        self.assertFalse(created)
        error_type = errs.get("error_type")
        self.assertEqual(
            error_type, [SerializerErrors.CreateWishlist.errors.get("description")]
        )
