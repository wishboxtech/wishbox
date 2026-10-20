from django.test import TestCase

from src.apps.website.models.contact_us import ContactUs
from src.apps.website.repositories.queries import get_contact_us
from src.utils.fakers import ContactUsFactory


class TestGetContactUsSelector(TestCase):
    def setUp(self):
        self.contact_us = ContactUsFactory()

    def test_get_contact_us(self):
        """Ensure the selector fetches the ContactUs instance."""
        fetched_contact = get_contact_us()
        self.assertEqual(fetched_contact, self.contact_us)

    def test_get_contact_us_no_instance(self):
        ContactUs.objects.all().delete()
        self.assertIsNone(get_contact_us())
