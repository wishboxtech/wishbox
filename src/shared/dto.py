from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DTO(BaseModel):
    """Explicit immutable boundary data; never carries an ORM object."""

    model_config = ConfigDict(frozen=True, extra="forbid")


class IdInputDTO(DTO):
    id: UUID


class DeleteOutputDTO(DTO):
    deleted: bool
