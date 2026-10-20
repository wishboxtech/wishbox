from django.utils import timezone

from src.apps.wishlist.models import GuestIdentity


class DjangoGuestRepository:
    def claim(self, key_hash, user_id):
        identity = (
            GuestIdentity.objects.select_for_update().filter(key_hash=key_hash).first()
        )
        if identity is None or identity.consumed_at is not None:
            return False
        if GuestIdentity.objects.filter(claimed_user_id=user_id).exists():
            return False
        identity.claimed_user_id = user_id
        identity.consumed_at = timezone.now()
        identity.save(update_fields=["claimed_user", "consumed_at"])
        return True
