from django.contrib.auth import get_user_model
from django.test import TestCase

from src.apps.authentication.selectors import create_user


class CreateUserSelectorTestCase(TestCase):
    def test_create_user_selector(self):
        user = create_user(
            phone_number="09999999999",
            password="foo",
        )
        User = get_user_model()
        self.assertEqual(type(user), User)
        self.assertTrue(
            User.objects.filter(
                phone_number="09999999999",
            ).exists()
        )
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password("foo"))
