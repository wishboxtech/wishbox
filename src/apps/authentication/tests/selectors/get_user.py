import uuid

from django.test import TestCase

from src.apps.authentication.selectors import get_user_by_id, get_user_by_phone_number
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
