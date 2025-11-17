import uuid

from django.test import TestCase

from src.apps.profile.models import Avatar
from src.apps.profile.selectors import get_user_avatar_settings
from src.utils.fakers import AvatarFactory, ProfileFactory


class GetUserAvatarSettingsTestCase(TestCase):
    def setUp(self):
        self.profile = ProfileFactory()
        self.avatar = AvatarFactory(profile=self.profile)

    def test_get_user_avatar_settings_returns_avatar(self):
        """Should return the Avatar object if it exists for given profile."""
        result = get_user_avatar_settings(self.profile.profile_id)

        self.assertIsInstance(result, Avatar)
        self.assertEqual(result.profile_id, self.profile.profile_id)

    def test_get_user_avatar_settings_returns_none_if_not_found(self):
        """Should return None when avatar does not exist for given profile."""
        missing_profile_id = uuid.uuid4()
        result = get_user_avatar_settings(missing_profile_id)
        self.assertIsNone(result)

    def test_get_user_avatar_settings_loads_only_settings_field(self):
        """Should load only 'settings' field (other fields deferred)."""
        result = get_user_avatar_settings(self.profile.profile_id)

        # Verify it's a valid Avatar
        self.assertIsInstance(result, Avatar)

        # Check deferred fields (everything except 'settings')
        deferred_fields = result.get_deferred_fields()
        self.assertIn("created_at", deferred_fields)
        self.assertIn("updated_at", deferred_fields)
        self.assertIn("profile_id", deferred_fields)
        self.assertNotIn("settings", deferred_fields)
