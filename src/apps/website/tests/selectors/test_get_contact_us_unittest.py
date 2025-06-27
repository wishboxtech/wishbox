from django.test import TestCase
from src.apps.website.selectors import get_contact_us
from src.utils.fakers import ContactUsFactory
from src.utils.exceptions import NotFoundException
from src.apps.website.models.contact_us import ContactUs

class TestGetContactUsSelector(TestCase):
    def setUp(self):
        self.contact_us = ContactUsFactory()    

    def test_get_contact_us(self):
        """Ensure the selector fetches the ContactUs instance."""
        fetched_contact = get_contact_us()
        self.assertEqual(fetched_contact, self.contact_us)

    def test_get_contact_us_no_instance(self):
        ContactUs.objects.all().delete() 
        with self.assertRaises(NotFoundException) as context:
            get_contact_us()
            
        self.assertEqual(context.exception.message, {"detail": "ContactUs instance not found"})
        self.assertEqual(context.exception.error_type, [["not_found"]])

        