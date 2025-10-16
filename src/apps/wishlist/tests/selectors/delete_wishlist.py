import uuid

from django.test import TestCase
from faker import Faker

from src.apps.wishlist.models import Wishlist
from src.apps.wishlist.selectors import delete_wishlist_by_id
from src.utils.fakers import WishlistFactory


class DeleteWishlistByIdSelectorTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.wishlist = WishlistFactory(
            name=self.faker.word(),
            description=self.faker.text(),
        )

    def test_delete_wishlist_by_valid_uuid(self):
        """Should delete the wishlist and return True when given a valid UUID."""
        result = delete_wishlist_by_id(self.wishlist.id)
        self.assertTrue(result)
        self.assertFalse(Wishlist.objects.filter(id=self.wishlist.id).exists())

    def test_delete_wishlist_by_valid_string_id(self):
        """Should delete the wishlist when given the ID as a string."""
        wishlist = WishlistFactory()
        result = delete_wishlist_by_id(str(wishlist.id))
        self.assertTrue(result)
        self.assertFalse(Wishlist.objects.filter(id=wishlist.id).exists())

    def test_delete_wishlist_by_nonexistent_uuid(self):
        """Should return False if the wishlist with given UUID does not exist."""
        non_existent_id = uuid.uuid4()
        result = delete_wishlist_by_id(non_existent_id)
        self.assertFalse(result)

    def test_delete_wishlist_by_nonexistent_string_id(self):
        """Should return False if the wishlist with given string UUID does not exist."""
        non_existent_id = str(uuid.uuid4())
        result = delete_wishlist_by_id(non_existent_id)
        self.assertFalse(result)

    def test_delete_wishlist_does_not_raise_error_on_missing(self):
        """Should not raise an exception if the wishlist does not exist."""
        try:
            delete_wishlist_by_id(uuid.uuid4())
        except Exception as e:
            self.fail(f"Function raised an exception unexpectedly: {e}")
