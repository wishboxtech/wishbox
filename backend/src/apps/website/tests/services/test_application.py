from django.test import TestCase

from src.apps.website.dto import ListContactsInputDTO
from src.core.composition import website_service
from src.shared.domain.errors import NotFound
from src.utils.fakers import ContactUsFactory


class TestGetContactUsService(TestCase):
    def test_contact_returns_dto(self):
        item = ContactUsFactory()
        result = website_service().list_contacts(ListContactsInputDTO())
        self.assertEqual(result[0].email, item.email)

    def test_empty_contacts_raise_domain_error(self):
        with self.assertRaises(NotFound):
            website_service().list_contacts(ListContactsInputDTO())
