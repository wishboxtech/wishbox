import uuid

from django.test import TestCase
from faker import Faker

from src.apps.wishlist.selectors import get_wishes_by_wishlist_id
from src.utils.fakers import WishFactory, WishlistFactory


class GetWishesSelectorTestCase(TestCase):

    def setUp(self):
        self.faker = Faker()
        self.wishlist = WishlistFactory()
        self.wishes = WishFactory.create_batch(5, wishlist_id=self.wishlist.id)

    def test_get_wishlists_by_profile_id(self):
        wishlists = get_wishes_by_wishlist_id(
            wishlist_id=self.wishlist.id,
        )
        self.assertEqual(wishlists.count(), 5)

    def test_get_empty_wishlists(self):
        wishlists = get_wishes_by_wishlist_id(wishlist_id=uuid.uuid4())
        self.assertEqual(wishlists.count(), 0)
