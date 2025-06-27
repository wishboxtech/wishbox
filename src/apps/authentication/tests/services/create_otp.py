from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase

from src.apps.authentication.services import create_one_time_password
from src.utils.fakers import UserFactory


class CreateOneTimePasswordServiceTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    @patch("src.apps.authentication.services.create_otp.send_sms_otp")
    def test_create_one_time_password_service(self, *_):
        otp_id = create_one_time_password(phone_number=self.user.phone_number)
        self.assertNotEqual(0, cache.ttl(self.user.phone_number))
        self.assertNotEqual(0, cache.ttl(otp_id))
