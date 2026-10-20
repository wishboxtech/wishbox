"""Run the native development server on the port configured in .env.local."""

import os
from pathlib import Path
import sys
from dotenv import load_dotenv

root = Path(__file__).resolve().parent.parent
load_dotenv(root.parent / ".env.local")
os.environ["STAGE"] = "local"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
sys.path.insert(0, str(root))

from django.core.management import execute_from_command_line

execute_from_command_line(
    ["manage.py", "runserver", f"0.0.0.0:{os.environ.get('API_PORT', '8000')}"]
)
