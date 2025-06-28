from django.test import TestCase

from src.apps.authentication.services import get_user_id_by_phone_number
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
