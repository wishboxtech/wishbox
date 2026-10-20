from uuid import UUID

from src.apps.wishlist.gifting_interfaces import GiftCredentials
from src.apps.wishlist.guest_interfaces import GuestRepository
from src.shared.interfaces import TransactionBoundary


class GuestClaimService:
    """Called only inside the transaction that creates a new account."""

    def __init__(
        self,
        repository: GuestRepository,
        credentials: GiftCredentials,
        transaction: TransactionBoundary,
    ):
        self.repository = repository
        self.credentials = credentials
        self.transaction = transaction

    def claim(self, key: str, user_id: UUID) -> bool:
        if not key:
            return False
        with self.transaction():
            return self.repository.claim(self.credentials.digest(key), user_id)
