from typing import Annotated
from uuid import UUID

from pydantic import Field

from src.shared.dto import DTO


class UploadMediaInputDTO(DTO):
    filename: Annotated[str, Field(min_length=1)]
    content: bytes


class MediaOutputDTO(DTO):
    file: str


class UploadMediaOutputDTO(DTO):
    media_id: UUID
