from concurrent.futures import ThreadPoolExecutor
from threading import Event
from unittest import skipUnless

from django.db import connection, connections
from django.test import TransactionTestCase

from src.apps.profile.dto import UpdateAvatarInputDTO
from src.core.composition import profile_service
from src.utils.fakers import AvatarFactory


@skipUnless(connection.vendor == "postgresql", "Row locking requires PostgreSQL")
class AvatarLockingTests(TransactionTestCase):
    def test_concurrent_patches_preserve_both_updates(self):
        avatar = AvatarFactory()
        first_has_lock, release_first, second_started, second_saved = (
            Event() for _ in range(4)
        )

        def update_first():
            service = profile_service()
            save = service.repository.save_avatar

            def paused_save(id, settings):
                first_has_lock.set()
                if not release_first.wait(5):
                    raise RuntimeError("Timed out waiting for the locking test")
                save(id, settings)

            service.repository.save_avatar = paused_save
            try:
                service.update_avatar(
                    UpdateAvatarInputDTO(
                        profile_id=avatar.profile_id,
                        changes={"background": {"color": "red"}},
                    )
                )
            finally:
                connections.close_all()

        def update_second():
            service = profile_service()
            save = service.repository.save_avatar

            def observed_save(id, settings):
                second_saved.set()
                save(id, settings)

            service.repository.save_avatar = observed_save
            second_started.set()
            try:
                service.update_avatar(
                    UpdateAvatarInputDTO(
                        profile_id=avatar.profile_id, changes={"gender": "female"}
                    )
                )
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            first = pool.submit(update_first)
            try:
                self.assertTrue(first_has_lock.wait(5))
                second = pool.submit(update_second)
                self.assertTrue(second_started.wait(5))
                self.assertFalse(
                    second_saved.wait(0.2), "Second update bypassed the row lock"
                )
            finally:
                release_first.set()
            first.result(timeout=5)
            second.result(timeout=5)
        avatar.refresh_from_db()
        self.assertEqual(avatar.settings["background"]["color"], "red")
        self.assertEqual(avatar.settings["gender"], "female")
