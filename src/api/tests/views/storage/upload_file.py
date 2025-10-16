from django.test import LiveServerTestCase
from django.urls import reverse
from rest_framework.test import RequestsClient

from src.apps.authentication.services import login_user_by_id
from src.static import ErrorEnum
from src.utils.fakers import UserFactory, fake_image


class UploadFileViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()
        self.user = UserFactory()
        self.access = login_user_by_id(user_id=self.user.id).get("access_token")

    def make_request(self, headers=None, data=None, files=None):
        url = self.live_server_url + reverse("upload_media")
        return self.rc.post(
            url,
            json=data,
            headers=headers,
            files=files,
        )

    def test_unauthorized(self):
        response = self.make_request()
        self.assertEqual(response.status_code, 401)

    def test_bad_request_response(self):
        response = self.make_request(headers={"access": self.access})
        self.assertEqual(response.status_code, 400)
        error = [ErrorEnum.UploadFile.FILE_IS_EMPTY]
        data_error = response.json().get("error_type")
        self.assertListEqual(error, data_error)

    def test_created_response(self):
        file = fake_image()
        files = {"file": file}
        response = self.make_request(files=files, headers={"access": self.access})
        self.assertEqual(response.status_code, 201)
