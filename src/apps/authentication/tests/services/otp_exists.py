from unittest.mock import patch

from django.test import TestCase

from src.apps.authentication.services import (create_one_time_password,
                                              one_time_password_exists)
from src.utils.fakers import UserFactory


class OTPExistServiceTestCase(TestCase):
    @patch("src.apps.authentication.services.create_otp.send_sms_otp")
    def setUp(self, *_):
        self.user = UserFactory()
        create_one_time_password(phone_number=self.user.phone_number)

    def test_create_one_time_password_service(self):
        self.assertTrue(one_time_password_exists(phone_number=self.user.phone_number))
        with patch("django.core.cache.cache.ttl", new=lambda x: 0):
            self.assertFalse(
                one_time_password_exists(phone_number=self.user.phone_number)
            )
