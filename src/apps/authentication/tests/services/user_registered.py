import uuid

from django.test import TestCase

from src.apps.authentication.services import user_registered
from src.utils.fakers import UserFactory
from src.utils.exceptions import InvalidUserID


class UserRegisteredServiceTestCase(TestCase):
    def setUp(self):
        self.registered_user = UserFactory(gender="M", birth_date="2024-03-23")
        self.unregistered_user = UserFactory(province=None, gender="")

    def test_user_registered_service(self):
        self.assertEqual(
            "sign_in",
            user_registered(user_id=self.registered_user.id),
        )
        self.assertEqual(
            "sign_up",
            user_registered(user_id=self.unregistered_user.id),
        )
        fake_id = uuid.uuid4()
        with self.assertRaises(InvalidUserID):
            user_registered(user_id=fake_id)
