import uuid

from django.test import TestCase
from django.utils import timezone
from faker import Faker
from src.static.serializer_errors import SerializerErrors
from src.apps.wallet.services import create_card
from src.utils.fakers import UserFactory


class CreateCardServiceTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_valid_create_card(self):
        valid_data = {
            "user": self.user.id,
            "card_number": "1111222233334444",
        }

        card, errs, done = create_card(data=valid_data)
        self.assertEqual(card.get("user"), self.user.id)
        self.assertDictEqual(errs, {})
        self.assertTrue(done)

    def test_invalid_create_card(self):
        invalid_data = {
            "user": uuid.uuid4(),
            "card_number": "1111222233334444",
        }

        _, errs, done = create_card(data=invalid_data)
        self.assertEqual(
            [SerializerErrors.CreateCard.errors.get("user")],
            errs["error_type"],
        )
        self.assertFalse(done)

        invalid_data = {
            "user": self.user.id,
            "card_number": "111122223333444",
        }

        _, errs, done = create_card(data=invalid_data)
        self.assertEqual(
            [SerializerErrors.CreateCard.errors.get("card_number")],
            errs["error_type"],
        )
        self.assertFalse(done)
