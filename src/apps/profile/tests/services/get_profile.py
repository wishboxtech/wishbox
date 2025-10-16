import faker
from django.test import TestCase

from src.apps.profile.selectors import get_profile_by_id
from src.apps.profile.serializers.profile import ReadProfileSerializer
from src.apps.profile.services import get_profile_by_user_id
from src.utils.fakers import ProfileFactory, UserFactory


class GetProfileById(TestCase):
    def setUp(self):
        self.user_with_profile = UserFactory()
        self.user_without_profile = UserFactory()
        self.profile = ProfileFactory(profile_id=self.user_with_profile.id)

    def test_get_profile_by_user_id_with_profile(self):
        """Should return serialized profile data when profile exists"""
        result = get_profile_by_user_id(self.user_with_profile.id)
        profile = get_profile_by_id(self.profile.profile_id)
        expected_data = ReadProfileSerializer(instance=profile).data

        self.assertIsNotNone(result)
        self.assertEqual(result, expected_data)
        self.assertEqual(result["profile_id"], self.user_with_profile.id)

    def test_get_profile_by_user_id_without_profile(self):
        """Should return None when no profile exists"""
        result = get_profile_by_user_id(self.user_without_profile.id)
        self.assertIsNone(result)
