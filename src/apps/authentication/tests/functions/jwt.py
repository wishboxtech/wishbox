import uuid
from datetime import timedelta

import jwt
from django.core.cache import cache
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from settings import ACCESS_TTL, JWT_SECRET, REFRESH_TTL
from src.apps.authentication.functions import (claim_token, login, refresh,
                                               validate_token)
from src.utils.exceptions import InvalidRefresh
from src.utils.fakers import UserFactory


class JWTFunctionsTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def create_token(self, payload, ttl):
        token = jwt.encode(
            payload=payload,
            key=JWT_SECRET,
            algorithm="HS512",
        )
        cache.set(token, "", timeout=ttl)
        return token

    def decode_token(self, token):
        return jwt.decode(token, key=JWT_SECRET, algorithms=["HS512"])

    def test_login_jwt_function(self):
        user_id = str(self.user.id)
        tokens = login(self.user)
        access_token, refresh_token = (
            tokens.get("access_token"),
            tokens.get("refresh_token"),
        )
        access_data = self.decode_token(token=access_token)
        refresh_data = self.decode_token(token=refresh_token)

        self.assertNotEqual(cache.ttl(access_token), 0)
        self.assertNotEqual(cache.ttl(refresh_token), 0)

        self.assertEqual(access_data.get("type"), "access")
        self.assertEqual(access_data.get("user_id"), user_id)

        self.assertEqual(refresh_data.get("access"), access_token)
        self.assertEqual(refresh_data.get("type"), "refresh")
        self.assertEqual(refresh_data.get("user_id"), user_id)

    def test_claim_token_jwt_function(self):
        tokens = login(
            self.user,
            extra_data={"parental_control": True, "selected_age": 12},
        )
        access_token, refresh_token = (
            tokens.get("access_token"),
            tokens.get("refresh_token"),
        )
        access_data = self.decode_token(token=access_token)
        refresh_data = self.decode_token(token=refresh_token)
        access_claimed = claim_token(token=access_token)
        refresh_claimed = claim_token(token=refresh_token)
        self.assertEqual(access_data, access_claimed)
        self.assertEqual(refresh_data, refresh_claimed)

    def test_validate_token_jwt_function_with_inavlid_token(self):

        self.assertFalse(validate_token(token="not cacehd"))

        cache.set("invalid cached token", "", timeout=ACCESS_TTL)
        self.assertFalse(validate_token(token="invalid cached token"))

    def test_validate_token_jwt_function_with_inavlid_data(self):
        created_at = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        user_id = str(self.user.id)
        invalid_access_with_missing_type = self.create_token(
            payload={
                "created_at": created_at,
                "extra_data": {
                    "parental_control": False,
                    "selected_age": None,
                },
            },
            ttl=ACCESS_TTL,
        )
        self.assertFalse(validate_token(token=invalid_access_with_missing_type))

        invalid_token_with_invalid_type = self.create_token(
            payload={
                "created_at": created_at,
                "type": "invalid",
                "extra_data": {
                    "parental_control": False,
                    "selected_age": None,
                },
            },
            ttl=ACCESS_TTL,
        )
        self.assertFalse(validate_token(token=invalid_token_with_invalid_type))

        invalid_refresh_with_no_access = self.create_token(
            payload={
                "user_id": user_id,
                "created_at": created_at,
                "type": "refresh",
                "extra_data": {
                    "parental_control": False,
                    "selected_age": None,
                },
            },
            ttl=REFRESH_TTL * 60,
        )
        invalid_refresh_with_no_access = self.create_token(
            payload={
                "user_id": user_id,
                "created_at": created_at,
                "type": "refresh",
                "extra_data": {
                    "parental_control": False,
                    "selected_age": None,
                },
            },
            ttl=REFRESH_TTL * 60,
        )
        self.assertFalse(validate_token(token=invalid_refresh_with_no_access))

        refresh_with_invalid_access = self.create_token(
            payload={
                "user_id": user_id,
                "created_at": created_at,
                "type": "refresh",
                "access": invalid_access_with_missing_type,
                "extra_data": {
                    "parental_control": False,
                    "selected_age": None,
                },
            },
            ttl=REFRESH_TTL * 60,
        )
        self.assertFalse(validate_token(token=refresh_with_invalid_access))

        fake_id = str(uuid.uuid4())
        access_with_invalid_user = self.create_token(
            payload={
                "user_id": fake_id,
                "created_at": created_at,
                "type": "access",
                "extra_data": {
                    "parental_control": False,
                    "selected_age": None,
                },
            },
            ttl=ACCESS_TTL,
        )
        self.assertFalse(validate_token(token=access_with_invalid_user))

        valid_access = self.create_token(
            payload={
                "user_id": user_id,
                "created_at": created_at,
                "type": "access",
                "extra_data": {
                    "parental_control": False,
                    "selected_age": None,
                },
            },
            ttl=ACCESS_TTL,
        )

        refresh_with_invalid_user = self.create_token(
            payload={
                "user_id": fake_id,
                "created_at": created_at,
                "type": "refresh",
                "access": valid_access,
                "extra_data": {
                    "parental_control": False,
                    "selected_age": None,
                },
            },
            ttl=REFRESH_TTL * 60,
        )
        self.assertFalse(validate_token(token=refresh_with_invalid_user))

    def test_validate_token_jwt_function_with_valid_token(self):
        user_id = str(self.user.id)
        created_at = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        valid_access = self.create_token(
            payload={
                "user_id": user_id,
                "created_at": created_at,
                "type": "access",
                "extra_data": {
                    "parental_control": True,
                    "selected_age": 12,
                },
            },
            ttl=ACCESS_TTL,
        )
        valid_refresh = self.create_token(
            payload={
                "user_id": user_id,
                "created_at": created_at,
                "type": "refresh",
                "access": valid_access,
                "extra_data": {
                    "parental_control": True,
                    "selected_age": 12,
                },
            },
            ttl=REFRESH_TTL * 60,
        )
        self.assertTrue(validate_token(token=valid_access))
        self.assertTrue(validate_token(token=valid_refresh))

        with freeze_time(timezone.now() + timedelta(seconds=ACCESS_TTL + 1)):
            self.assertFalse(validate_token(valid_access))
        with freeze_time(timezone.now() + timedelta(minutes=REFRESH_TTL * 60 + 1)):
            self.assertFalse(validate_token(token=valid_refresh))

    def test_refresh_token_jwt_function(self):
        tokens = login(self.user)
        with freeze_time(timezone.now() + timedelta(seconds=2)):
            new_access_token, new_refresh_token = refresh(tokens.get("refresh_token"))
        self.assertTrue(validate_token(new_access_token))
        self.assertTrue(validate_token(new_refresh_token))
        self.assertEqual(cache.ttl(tokens.get("access_token")), 10)
        self.assertEqual(cache.ttl(tokens.get("refresh_token")), 0)
        with self.assertRaises(InvalidRefresh):
            refresh(tokens.get("refresh_token"))  # refresh_token is now invalid
        with self.assertRaises(InvalidRefresh):
            refresh(new_access_token)  # access is not refresh
