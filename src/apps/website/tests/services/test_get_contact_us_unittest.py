from django.test import TestCase

from src.apps.website.models import ContactUs
from src.apps.website.selectors import get_contact_us
from src.apps.website.serializers import ContactUsSerializer
from src.utils.exceptions import NotFoundException
from src.utils.fakers import ContactUsFactory


class TestGetContactUsService(TestCase):
    def setUp(self):
        # ایجاد یک نمونه از ContactUs برای تست
        self.contact_us = ContactUsFactory()

    def test_get_contact_us_service(self):
        """Ensure the selector returns the correct ContactUs instance."""
        expected = ContactUsSerializer(self.contact_us).data
        fetched_contact = get_contact_us()
        self.assertEqual(fetched_contact.email, expected["email"])

    def test_get_contact_us_no_instance(self):
        """Ensure the selector raises an exception when no instance exists."""
        ContactUs.objects.all().delete()

        with self.assertRaises(NotFoundException) as context:
            get_contact_us()

        self.assertEqual(
            context.exception.message, {"detail": "ContactUs instance not found"}
        )
        self.assertEqual(context.exception.error_type, [["not_found"]])
