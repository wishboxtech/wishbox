from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class User:
    id: UUID
    phone_number: str | None
    email: str | None
    is_active: bool
    is_phone_number_verified: bool
    has_accepted_terms: bool
