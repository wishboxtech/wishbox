import uuid

from django.test import TestCase

from src.apps.authentication.functions import claim_token, validate_token
from src.apps.authentication.services import login_user_by_id
from src.utils.fakers import UserFactory


class LoginUserServiceTestCase(TestCase):
    def setUp(self):
        self.user_inactive = UserFactory()
        self.user_active = UserFactory(is_active=True)

    def test_login_user_by_id_service(self):
        self.assertIsNone(login_user_by_id(uuid.uuid4()))
        tokens = login_user_by_id(user_id=self.user_active.id)
        self.assertTrue(validate_token(token=tokens.get("access_token")))
        self.assertTrue(validate_token(token=tokens.get("refresh_token")))
