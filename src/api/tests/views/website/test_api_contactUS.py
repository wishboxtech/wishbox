from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from src.apps.website.models import ContactUs


class ContactUsAPIViewTest(APITestCase):

    def setUp(self):
        self.contact = ContactUs.objects.create(
            email="boz@abru.com"
        )
        self.url = reverse('contact_us_api')

    def test_get_contact_us_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data[0])

    def test_get_contact_us_not_found(self):
        ContactUs.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'ContactUs instance not found')
