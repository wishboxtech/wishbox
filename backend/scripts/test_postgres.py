"""Load explicit local database credentials before isolated PostgreSQL tests."""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv

root = Path(__file__).resolve().parent.parent
load_dotenv(root.parent / ".env.local")
os.environ["STAGE"] = "ci"
os.environ["WISHBOX_TEST_DB"] = "postgres"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
sys.path.insert(0, str(root))

from django.core.management import execute_from_command_line

execute_from_command_line(["manage.py", "test", "src.apps", "src.api", "--noinput"])
