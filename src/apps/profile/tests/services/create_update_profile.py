import faker

from django.test import TestCase

from src.apps.profile.services import create_or_update_profile
from src.utils.fakers import UserFactory, ProfileFactory


class CreateUpdateProfileTestCase(TestCase):
    def setUp(self):
        self.user_with_profile = UserFactory()
        self.user_without_profile = UserFactory()
        self.profile = ProfileFactory(profile_id=self.user_with_profile.id)

    def test_create_profile(self):
        created, data, _ = create_or_update_profile(
            self.user_without_profile.id,
            {
                "profile": self.user_without_profile.id,
                "first_name": faker.Faker().first_name(),
                "last_name": faker.Faker().last_name(),
            },
        )
        self.assertTrue(created)
        self.assertIsNotNone(data.get("first_name"))
        self.assertIsNotNone(data.get("last_name"))
        self.assertEqual(data.get("profile_id"), self.user_without_profile.id)

    def test_update_profile(self):
        first_name_to_change = faker.Faker().first_name()
        last_name_to_change = faker.Faker().last_name()
        self.assertNotEqual(self.profile.first_name, first_name_to_change)
        self.assertNotEqual(self.profile.last_name, last_name_to_change)
        created, data, _ = create_or_update_profile(
            self.user_with_profile.id,
            {
                "profile": self.user_with_profile.id,
                "first_name": first_name_to_change,
                "last_name": last_name_to_change,
            },
        )
        self.assertFalse(created)
        self.assertEqual(self.profile.profile_id, data.get("profile_id"))
        self.assertEqual(first_name_to_change, data.get("first_name"))
        self.assertEqual(last_name_to_change, data.get("last_name"))
