from django.db.models.query import QuerySet

from django.test import TestCase

from src.apps.wishlist.selectors import get_wishlists_by_profile
from src.utils.fakers import WishlistFactory, ProfileFactory
from faker import Faker


class GetWishlistsSelectorTestCase(TestCase):

    def setUp(self):
        self.faker = Faker()
        self.profile = ProfileFactory()
        self.profile_no_wish = ProfileFactory()
        self.wishlists = WishlistFactory.create_batch(5, profile=self.profile)

    def test_get_wishlists_by_profile_id(self):
        wishlists = get_wishlists_by_profile(profile_id=self.profile.profile_id)
        self.assertEqual(wishlists.count(), 5)

    def test_get_empty_wishlists(self):
        wishlists = get_wishlists_by_profile(profile_id=self.profile_no_wish.profile_id)
        self.assertEqual(wishlists.count(), 0)
