import uuid

from django.test import TestCase

from src.apps.profile.selectors import get_profile_by_id
from src.utils.fakers import ProfileFactory
from faker import Faker


class GetProfileSelectorTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.random_first_name = self.faker.first_name()
        self.profile = ProfileFactory(first_name=self.random_first_name)
        self.fake_id = uuid.uuid4()

    def test_get_profile_by_id(self):
        profile = get_profile_by_id(self.profile.profile_id)
        self.assertEqual(profile.first_name, self.random_first_name)
        self.assertEqual(profile.profile_id, self.profile.profile_id)

    def test_get_invalid_profile(self):
        profile = get_profile_by_id(self.fake_id)
        self.assertIsNone(profile)
