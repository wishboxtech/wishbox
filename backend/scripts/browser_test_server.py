"""Disposable local HTTP server for browser tests; never uses the development DB."""
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

os.environ["STAGE"] = "ci"
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
# A short, real expiry lets the browser test log in again without waiting for
# the intentionally very long OTP lifetime used by unit-test fixtures.
os.environ["OTP_TTL"] = "15"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from django.conf import settings

with TemporaryDirectory(prefix="wishy-browser-") as folder:
    settings.DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(Path(folder) / "browser.sqlite3"),
        }
    }
    import django

    django.setup()
    from django.core.management import call_command
    from src.utils.fakers import (
        UserFactory,
        ProfileFactory,
        WishlistFactory,
        WishFactory,
    )

    call_command("migrate", verbosity=0)
    user = UserFactory(phone_number="09123450901")
    profile = ProfileFactory(
        profile_id=user.id, first_name="Sara", last_name="", bio=""
    )
    wishlist = WishlistFactory(
        profile=profile, name="Birthday wishes", description="چند تا چیز که دوست دارم"
    )
    wishes = [
        WishFactory(
            wishlist=wishlist,
            name=name,
            description="Purple, adjustable · رنگ بنفش",
            price=1250000,
        )
        for name in ("Reading lamp", "A cozy blanket")
    ]
    Path(os.environ.get("WISHY_LIVE_DATA", "/tmp/wishy-live-data.json")).write_text(
        json.dumps(
            {
                "owner_phone": user.phone_number,
                "list_id": str(wishlist.id),
                "wish_ids": [str(w.id) for w in wishes],
            }
        )
    )
    print("Disposable browser test API: http://127.0.0.1:8012", flush=True)
    call_command("runserver", "127.0.0.1:8012", use_reloader=False, use_threading=False)
