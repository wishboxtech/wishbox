import uuid

from django.test import TestCase
from factory.faker import faker

from src.apps.authentication.selectors import user_with_id_exist
from src.utils.fakers import UserFactory


class UserExistsSelectorTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_user_with_id_exist_selector(self):
        fake_id = uuid.uuid4()
        exists = user_with_id_exist(user_id=fake_id)
        self.assertFalse(exists)
        not_exists = user_with_id_exist(user_id=self.user.id)
        self.assertTrue(not_exists)
