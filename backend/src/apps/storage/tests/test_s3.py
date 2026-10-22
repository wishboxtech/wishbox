from urllib.parse import parse_qs, urlsplit

from botocore.stub import Stubber
from django.core.files.storage import default_storage
from django.test import TestCase, override_settings

from settings.storage import media_storage_settings
from src.apps.storage.dto import UploadMediaInputDTO
from src.apps.storage.models import MediaModel
from src.core.composition import storage_service
from src.shared.dto import IdInputDTO


S3_SETTINGS = media_storage_settings(
    {
        "USE_S3": "True",
        "S3_ENDPOINT_URL": "https://s3.example.test",
        "S3_REGION_NAME": "test-region",
        "S3_BUCKET_NAME": "wishy",
        "S3_ACCESS_KEY_ID": "test-access",
        "S3_SECRET_ACCESS_KEY": "test-secret",
    }
)


@override_settings(STORAGES=S3_SETTINGS)
class S3MediaTests(TestCase):
    def test_upload_uses_s3_and_read_returns_a_signed_https_url(self):
        client = default_storage.connection.meta.client
        with Stubber(client) as stub:
            stub.add_client_error(
                "head_object", service_error_code="404", http_status_code=404
            )
            stub.add_response("put_object", {"ETag": '"test-etag"'})
            uploaded = storage_service().upload(
                UploadMediaInputDTO(filename="hello.txt", content=b"hello from Wishy")
            )
            media = storage_service().get(IdInputDTO(id=uploaded.media_id))
            stub.assert_no_pending_responses()
        item = MediaModel.objects.get(pk=uploaded.media_id)
        url = urlsplit(media.file)
        self.assertEqual(url.scheme, "https")
        self.assertEqual(url.netloc, "s3.example.test")
        self.assertEqual(url.path, f"/wishy/{item.file.name}")
        params = parse_qs(url.query)
        self.assertEqual(params["X-Amz-Algorithm"], ["AWS4-HMAC-SHA256"])
        self.assertEqual(params["X-Amz-Expires"], ["3600"])
        self.assertIn("/test-region/s3/aws4_request", params["X-Amz-Credential"][0])
        self.assertNotIn("test-secret", media.file)
