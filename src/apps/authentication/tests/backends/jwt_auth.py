from django.test import TestCase
from rest_framework.test import APIRequestFactory

from src.apps.authentication.backends import JWTAuthentication
from src.apps.authentication.functions import login
from src.utils.fakers import UserFactory


class JWTAuthenticationBackendTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.access = login(self.user).get("access_token")
        self.auth_class = JWTAuthentication()

    def test_jwt_auth_backend(self):
        def create_request(HTTP_ACCESS=None):
            return self.factory.get("/examlple", data=None, HTTP_ACCESS=HTTP_ACCESS)

        request_fail = create_request()
        self.assertIsNone(self.auth_class.authenticate(request_fail))

        request_raise = create_request(HTTP_ACCESS="invalid")
        self.assertIsNone(self.auth_class.authenticate(request_raise))

        request_success = create_request(HTTP_ACCESS=self.access)
        self.assertEqual(self.auth_class.authenticate(request_success)[0], self.user)

    def test_jwt_with_parental_control(self):
        def create_request(HTTP_ACCESS=None):
            return self.factory.get("/examlple", data=None, HTTP_ACCESS=HTTP_ACCESS)

        user = UserFactory()
        access = login(
            user=user,
            extra_data={"parental_control": True, "selected_age": 12},
        ).get("access_token")
        request_success = create_request(HTTP_ACCESS=access)
        user_data = self.auth_class.authenticate(request_success)[0]
        self.assertEqual(user_data, user)
        self.assertTrue(user_data.parental_control)
