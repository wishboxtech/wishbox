from django.test import TestCase
from django.core.exceptions import ValidationError
from src.apps.website.models.contact_us import ContactUs
from src.utils.fakers import ContactUsFactory

class TestContactUsModel(TestCase):
    def setUp(self):
        ContactUs.objects.all().delete()

    def test_create_contact_us(self):
        """check for create a record for contactUs model"""
        contact_us = ContactUsFactory.create()
        self.assertIsInstance(contact_us, ContactUs)
        self.assertIsNotNone(contact_us)

    def test_single_instance_constraint(self):
        """ensure that only one contact can be"""
        ContactUsFactory.create()

        contact_us = ContactUsFactory.build()
        with self.assertRaises(ValidationError):
            contact_us.full_clean()
