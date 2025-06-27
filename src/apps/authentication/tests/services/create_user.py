from django.contrib.auth import get_user_model
from django.test import TestCase

from src.apps.authentication.services import create_user


class CreateUserServiceTestCase(TestCase):
    def test_create_user_service(self):
        done, user_id, err = create_user(
            phone_number="09999999999",
            password="foo",
        )

        self.assertIsNone(err)
        self.assertIsNotNone(user_id)
        self.assertTrue(done)
        User = get_user_model()
        self.assertTrue(
            User.objects.filter(
                phone_number="09999999999",
            ).exists()
        )

        user = User.objects.get(id=user_id)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password("foo"))
        done, user_id, err = create_user(phone_number="invalid", password="foo")
        self.assertIsNotNone(err)
        self.assertIsNone(user_id)
        self.assertFalse(done)
