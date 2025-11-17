import uuid

from django.test import TestCase

from src.apps.authentication.selectors import (
    get_user_by_email_or_phone,
    get_user_by_id,
    get_user_by_phone_number,
)
from src.utils.fakers import UserFactory


class GetUserSelectorTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.fake_id = uuid.uuid4()

    def test_get_user_by_id_selector(self):
        user = get_user_by_id(user_id=self.user.id)
        self.assertEqual(self.user, user)
        self.assertIsNone(get_user_by_id(self.fake_id))

    def test_get_user_by_phone_number_selector(self):
        user = get_user_by_phone_number(phone_number=self.user.phone_number)
        self.assertEqual(self.user, user)
        self.assertIsNone(get_user_by_phone_number(self.fake_id))

    def test_get_user_by_email_or_phone_with_phone(self):
        """Should return user when valid phone number is given."""
        user = get_user_by_email_or_phone(self.user.phone_number)
        self.assertEqual(user, self.user)

        """Should return user when valid email is given."""
        user = get_user_by_email_or_phone(self.user.email)
        self.assertEqual(user, self.user)

        """Should return None when neither phone nor email match."""
        user = get_user_by_email_or_phone("invliad")
        self.assertIsNone(user)
