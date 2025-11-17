from django.test import TestCase

from src.apps.authentication.services import (
    get_user_id_by_identifier,
    get_user_id_by_phone_number,
)
from src.utils.fakers import UserFactory


class GetUserIDServiceTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_get_user_id_by_phone_number_service(self):
        self.assertEqual(
            self.user.id,
            get_user_id_by_phone_number(phone_number=self.user.phone_number),
        )
        self.assertIsNone(get_user_id_by_phone_number(phone_number="invalid"))

    def test_get_user_id_by_identifier_with_email(self):
        """Should return user.id when valid email is provided."""
        user_id = get_user_id_by_identifier(self.user.email)
        self.assertEqual(user_id, self.user.id)

    def test_get_user_id_by_identifier_with_phone_number(self):
        """Should return user.id when valid phone number is provided."""
        user_id = get_user_id_by_identifier(self.user.phone_number)
        self.assertEqual(user_id, self.user.id)

    def test_get_user_id_by_identifier_with_invalid_identifier(self):
        """Should return None when no user matches identifier."""
        user_id = get_user_id_by_identifier("invalid")
        self.assertIsNone(user_id)
