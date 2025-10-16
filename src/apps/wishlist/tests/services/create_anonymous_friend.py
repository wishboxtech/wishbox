import faker
from django.test import TestCase

from src.apps.wishlist.models import AnonymousFriend
from src.apps.wishlist.services import create_anonymous_friend
from src.static import SerializerErrors


class CreateAnonymousFriendTestCase(TestCase):
    def setUp(self):
        self.fake = faker.Faker()

    def test_create_anonymous_friend_valid(self):
        """Should create anonymous friend when nickname is provided"""
        nickname = self.fake.user_name()

        created, anonymous_friend_id, errs = create_anonymous_friend(
            {"nickname": nickname}
        )

        # Check success
        self.assertTrue(created)
        self.assertIsNotNone(anonymous_friend_id)
        self.assertEqual(errs, {})

        # Check that object exists in DB
        instance = AnonymousFriend.objects.get(id=anonymous_friend_id)
        self.assertEqual(instance.nickname, nickname)

    def test_create_anonymous_friend_invalid_missing_nickname(self):
        """Should fail when nickname is missing"""
        created, anonymous_friend_id, errs = create_anonymous_friend({})

        self.assertFalse(created)
        self.assertIsNone(anonymous_friend_id)

        # Validation errors should include nickname
        self.assertIn("errors", errs)
        self.assertIn("nickname", errs["errors"])
        self.assertIn("error_type", errs)

        # The reported error type should match SerializerErrors
        expected_error = SerializerErrors.CreateAnonymousFriend.errors.get("nickname")
        self.assertEqual(errs["error_type"], [expected_error])
