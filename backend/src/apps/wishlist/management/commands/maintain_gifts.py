import logging
import time
from pathlib import Path
from django.core.management.base import BaseCommand
from src.core.composition import gifting_service

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Release expired gift holds and send one private in-app planning reminder."

    def add_arguments(self, parser):
        parser.add_argument("--loop", action="store_true")
        parser.add_argument("--interval", type=int, default=60)

    def handle(self, *args, **options):
        while True:
            try:
                result = gifting_service().maintain(reminders=True)
                if result.expired or result.reminded:
                    self.stdout.write(
                        f"Gift maintenance: {result.expired} released, {result.reminded} reminded."
                    )
                if options["loop"]:
                    Path("/tmp/wishy-gifts-heartbeat").touch()
            except Exception:
                if not options["loop"]:
                    raise
                logger.exception("Gift maintenance failed; will retry.")
            if not options["loop"]:
                break
            time.sleep(max(1, options["interval"]))
