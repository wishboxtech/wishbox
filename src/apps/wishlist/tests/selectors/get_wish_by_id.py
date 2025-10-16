import uuid

from django.core.exceptions import ValidationError
from django.test import TestCase
from faker import Faker

from src.apps.wishlist.models import Wish
from src.apps.wishlist.selectors import get_wish_by_id
from src.utils.fakers import WishFactory


class GetWishByIdSelectorTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.wish = WishFactory(
            name=self.faker.word(),
            description=self.faker.text(),
            price=self.faker.random_int(min=100, max=5000),
        )

    def test_get_wish_by_valid_uuid(self):
        """Should return the wish object when given a valid UUID."""
        result = get_wish_by_id(self.wish.id)
        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.wish.id)
        self.assertEqual(result.name, self.wish.name)
        self.assertEqual(result.price, self.wish.price)
        self.assertIsInstance(result, Wish)

    def test_get_wish_by_valid_string_id(self):
        """Should return the wish when given the ID as a string."""
        result = get_wish_by_id(str(self.wish.id))
        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.wish.id)

    def test_get_wish_by_nonexistent_id(self):
        """Should return None if no wish with given ID exists."""
        non_existent_id = uuid.uuid4()
        result = get_wish_by_id(non_existent_id)
        self.assertIsNone(result)

    def test_get_wish_by_nonexistent_string_id(self):
        """Should return None if no wish with given string ID exists."""
        non_existent_id = str(uuid.uuid4())
        result = get_wish_by_id(non_existent_id)
        self.assertIsNone(result)

    def test_get_wish_by_invalid_id_format(self):
        """Should raise ValueError if ID format is invalid (not UUID)."""
        with self.assertRaises(ValidationError):
            get_wish_by_id("invalid-uuid")

    def test_only_fields_are_loaded(self):
        """Should only select specified fields and defer others."""
        result = get_wish_by_id(self.wish.id)
        # Check that only the declared fields are loaded
        deferred_fields = result.get_deferred_fields()
        # Assuming model has more fields (e.g., created_at, wishlist_id, etc.)
        self.assertTrue(
            len(deferred_fields) >= 1,
            msg="Expected at least one deferred field due to .only() usage.",
        )
