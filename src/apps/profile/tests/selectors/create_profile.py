import uuid

from django.test import TestCase

from src.utils.fakers import UserFactory
from src.apps.profile.selectors import create_profile

class CreateProfileSelectorTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_create_profile_selector(self):
        profile = create_profile(
            self.user.id
        )
        self.assertEqual(profile.profile_id, self.user.id)