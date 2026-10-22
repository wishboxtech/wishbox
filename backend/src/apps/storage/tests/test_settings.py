from unittest import TestCase

from settings.storage import media_storage_settings


class S3SettingsTests(TestCase):
    def settings(self, **overrides):
        return media_storage_settings(
            {
                "USE_S3": "True",
                "S3_ENDPOINT_URL": "https://s3.example.test/",
                "S3_BUCKET_NAME": "wishy",
                "S3_REGION_NAME": "test-region",
                "S3_ACCESS_KEY_ID": "test-access",
                "S3_SECRET_ACCESS_KEY": "test-secret",
                **overrides,
            }
        )

    def test_disabled_s3_needs_no_credentials_and_false_is_not_truthy(self):
        for value in ("False", "false", "0", "off", ""):
            with self.subTest(value=value):
                result = media_storage_settings({"USE_S3": value})
                self.assertEqual(
                    result["default"]["BACKEND"],
                    "django.core.files.storage.FileSystemStorage",
                )

    def test_s3_is_private_signed_and_keeps_admin_static_files_local(self):
        result = self.settings()
        options = result["default"]["OPTIONS"]
        self.assertEqual(options["endpoint_url"], "https://s3.example.test")
        self.assertEqual(options["bucket_name"], "wishy")
        self.assertEqual(options["signature_version"], "s3v4")
        self.assertTrue(options["querystring_auth"])
        self.assertFalse(options["file_overwrite"])
        self.assertIsNone(options["default_acl"])
        self.assertEqual(
            result["staticfiles"]["BACKEND"],
            "django.contrib.staticfiles.storage.StaticFilesStorage",
        )

    def test_missing_configuration_fails_without_revealing_secret(self):
        with self.assertRaisesRegex(ValueError, "S3_REGION_NAME") as error:
            self.settings(S3_REGION_NAME="")
        self.assertNotIn("test-secret", str(error.exception))

    def test_public_custom_domain_is_opt_in(self):
        result = self.settings(
            S3_QUERYSTRING_AUTH="False", S3_CUSTOM_DOMAIN="media.wishy.ir"
        )
        options = result["default"]["OPTIONS"]
        self.assertFalse(options["querystring_auth"])
        self.assertEqual(options["custom_domain"], "media.wishy.ir")
        with self.assertRaisesRegex(ValueError, "requires public media"):
            self.settings(S3_CUSTOM_DOMAIN="media.wishy.ir")

    def test_invalid_endpoint_bucket_boolean_and_expiry_fail_early(self):
        cases = [
            {"USE_S3": "perhaps"},
            {"S3_ENDPOINT_URL": "https://s3.example.test/wishy"},
            {"S3_ENDPOINT_URL": "https://user:secret@s3.example.test"},
            {"S3_BUCKET_NAME": "https://s3.example.test/wishy"},
            {"S3_ADDRESSING_STYLE": "invalid"},
            {"S3_QUERYSTRING_EXPIRE": "0"},
        ]
        for overrides in cases:
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                self.settings(**overrides)

    def test_legacy_minio_settings_can_still_supply_credentials(self):
        result = media_storage_settings(
            {
                "USE_S3": "True",
                "MINIO_STORAGE_ENDPOINT": "s3.example.test",
                "MINIO_STORAGE_MEDIA_BUCKET_NAME": "wishy",
                "MINIO_STORAGE_ACCESS_KEY": "test-access",
                "MINIO_STORAGE_SECRET_KEY": "test-secret",
                "S3_REGION_NAME": "test-region",
            }
        )
        self.assertEqual(
            result["default"]["OPTIONS"]["endpoint_url"], "https://s3.example.test"
        )
