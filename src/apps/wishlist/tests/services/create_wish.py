import faker
from django.test import TestCase

from src.apps.wishlist.services import create_wish
from src.static.serializer_errors import SerializerErrors
from src.utils.fakers import WishFactory, WishlistFactory


class CreateWishTestCase(TestCase):
    def setUp(self):
        self.wishlist = WishlistFactory()
        self.wish = WishFactory(
            wishlist=self.wishlist,
            name="PS5",
        )

    def test_create_wish(self):
        wish_name = faker.Faker().name()
        wish_description = faker.Faker().text()

        created, data, err = create_wish(
            {
                "wishlist": self.wishlist.id,
                "name": wish_name,
                "description": wish_description,
                "price": 10000,
            }
        )
        self.assertTrue(created)
        self.assertEqual(err, {})
        self.assertEqual(data.get("name"), wish_name)
        self.assertEqual(data.get("description"), wish_description)

    def test_invalid_create_wish(self):
        created, _, errs = create_wish(
            {
                "wishlist": self.wishlist.id,
                "description": None,
            },
        )
        self.assertFalse(created)
        error_type = errs.get("error_type")
        self.assertEqual(
            error_type, [SerializerErrors.CreateWish.errors.get("description")]
        )
