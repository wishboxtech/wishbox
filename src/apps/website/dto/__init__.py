from datetime import datetime
from uuid import UUID

from src.shared.dto import DTO


class ListContactsInputDTO(DTO):
    pass


class ContactOutputDTO(DTO):
    id: UUID
    email: str
    created_at: datetime
    updated_at: datetime
