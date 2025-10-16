import uuid

from django.test import TestCase
from faker import Faker

from src.apps.wishlist.models import Wish
from src.apps.wishlist.services import delete_wish
from src.utils.fakers import WishFactory


class DeleteWishByIdServiceTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.wish = WishFactory(
            name=self.faker.word(),
            description=self.faker.text(),
            price=self.faker.random_int(min=100, max=5000),
        )

    def test_delete_wish_by_valid_uuid(self):
        """Should delete the wish and return True when given a valid UUID."""
        result = delete_wish(self.wish.id)
        self.assertTrue(result)
        self.assertFalse(Wish.objects.filter(id=self.wish.id).exists())

    def test_delete_wish_by_valid_string_id(self):
        """Should delete the wish when given the ID as a string."""
        wish = WishFactory()
        result = delete_wish(str(wish.id))
        self.assertTrue(result)
        self.assertFalse(Wish.objects.filter(id=wish.id).exists())

    def test_delete_wish_by_nonexistent_uuid(self):
        """Should return False if the wish with given UUID does not exist."""
        non_existent_id = uuid.uuid4()
        result = delete_wish(non_existent_id)
        self.assertFalse(result)

    def test_delete_wish_by_nonexistent_string_id(self):
        """Should return False if the wish with given string UUID does not exist."""
        non_existent_id = str(uuid.uuid4())
        result = delete_wish(non_existent_id)
        self.assertFalse(result)

    def test_delete_wish_does_not_raise_error_on_missing(self):
        """Should not raise an exception if the wish does not exist."""
        try:
            delete_wish(uuid.uuid4())
        except Exception as e:
            self.fail(f"Function raised an exception unexpectedly: {e}")
