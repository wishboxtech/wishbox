from datetime import timedelta

from django.core.cache import cache
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from src.apps.authentication.functions import login, validate_token
from src.apps.authentication.services import refresh
from src.utils.fakers import UserFactory
from src.utils.exceptions import InvalidRefresh


class RefreshServiceTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_refresh_token_service(self):
        tokens = login(self.user)
        with freeze_time(timezone.now() + timedelta(seconds=2)):
            new_access_token, new_refresh_token = refresh(tokens.get("refresh_token"))
        self.assertTrue(validate_token(token=new_access_token))
        self.assertTrue(validate_token(token=new_refresh_token))
        self.assertEqual(cache.ttl(tokens.get("access_token")), 10)
        self.assertEqual(cache.ttl(tokens.get("refresh_token")), 0)
        with self.assertRaises(InvalidRefresh):
            refresh(tokens.get("refresh_token"))  # refresh_token is now invalid
        with self.assertRaises(InvalidRefresh):
            refresh(new_access_token)  # access is not refresh
