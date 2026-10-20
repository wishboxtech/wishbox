import os
import subprocess
import sys
from unittest import TestCase

from scripts.check_architecture import ROOT, check_modules, check_project


class ArchitectureTests(TestCase):
    def test_project_obeys_dependency_direction(self):
        self.assertEqual(check_project(), [])

    def test_checker_rejects_framework_import_in_service(self):
        self.assertTrue(
            check_modules(
                {"src.apps.wishlist.services.bad": "from django.db import transaction"}
            )
        )

    def test_checker_rejects_private_cross_app_repository_import(self):
        self.assertTrue(
            check_modules(
                {
                    "src.apps.wishlist.repositories.bad": "from src.apps.profile.models import Profile"
                }
            )
        )

    def test_checker_rejects_view_model_import(self):
        self.assertTrue(
            check_modules(
                {"src.api.views.bad": "from src.apps.wishlist.models import Wish"}
            )
        )

    def test_checker_rejects_app_serializers_and_their_imports(self):
        cases = [
            {"src.apps.profile.serializers.profile": "class ProfileSerializer: pass"},
            {
                "src.api.views.profile.profile": "from src.apps.profile.serializers import ProfileSerializer"
            },
        ]
        for modules in cases:
            with self.subTest(modules=modules):
                self.assertTrue(check_modules(modules))

    def test_checker_rejects_cycles(self):
        errors = check_modules(
            {
                "src.apps.wishlist.services.a": "import src.apps.wishlist.services.b",
                "src.apps.wishlist.services.b": "import src.apps.wishlist.services.a",
            }
        )
        self.assertTrue(any("Circular dependency" in error for error in errors))

    def test_all_services_import_with_framework_and_settings_blocked(self):
        code = """
import importlib.abc, sys
class BlockFramework(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'django', 'rest_framework', 'settings', 'jwt', 'nats', 'magic'}:
            raise AssertionError('Framework dependency: ' + fullname)
sys.meta_path.insert(0, BlockFramework())
for app in ('authentication', 'profile', 'storage', 'website', 'wishlist'):
    __import__('src.apps.' + app + '.services')
"""
        env = {
            key: value
            for key, value in os.environ.items()
            if key not in {"STAGE", "DJANGO_SETTINGS_MODULE"}
        }
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
