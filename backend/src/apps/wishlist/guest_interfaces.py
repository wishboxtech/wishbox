from typing import Protocol
from uuid import UUID


class GuestRepository(Protocol):
    def claim(self, key_hash: str, user_id: UUID) -> bool:
        ...
