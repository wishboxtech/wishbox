from django.test import LiveServerTestCase
from django.urls import reverse
from faker import Faker
from rest_framework.test import RequestsClient


class CreateAnonymousFriendAPIViewTestCase(LiveServerTestCase):
    
    def setUp(self):
        self.rc = RequestsClient()
        self.fake = Faker()
        self.url = self.live_server_url + reverse("create_anonymous_friend")
        
    def test_valid_create_anonymous_friend_api(self):
        body = {"nickname": self.fake.user_name()}
        response = self.rc.post(self.url, json=body)
        
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.json().get("anonymous_friend_id"))
        self.assertEqual(response.json().get("created"), True)
        
    def test_invalid_create_anonymous_friend_api(self):
        body = {"nickname": ""}
        response = self.rc.post(self.url, json=body)

        self.assertEqual(response.status_code, 400)