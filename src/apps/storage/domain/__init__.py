from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Media:
    id: UUID
    file: str
