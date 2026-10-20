from datetime import date
from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field, JsonValue

from src.apps.profile.domain.avatar import AvatarSettings, Background
from src.apps.profile.domain.cat import CatAvatar
from src.apps.storage.dto import MediaOutputDTO
from src.shared.dto import DTO


class UpsertProfileInputDTO(DTO):
    profile_id: UUID
    first_name: Annotated[str, Field(max_length=150)] | None = None
    last_name: Annotated[str, Field(max_length=150)] | None = None
    birthdate: date | None = None
    gender: Literal["male", "female", ""] | None = None
    bio: Annotated[str, Field(max_length=250)] | None = None
    photo_id: UUID | None = None
    cat_avatar: CatAvatar | None = None


class ProfileOutputDTO(DTO):
    profile_id: UUID
    phone_number: str | None
    email: str | None
    first_name: str | None
    last_name: str | None
    birthdate: date | None
    gender: str | None
    bio: str | None
    photo: MediaOutputDTO | None
    cat_avatar: CatAvatar | None = None
    is_phone_number_verified: bool
    has_accepted_terms: bool


class UpsertProfileOutputDTO(DTO):
    created: bool
    profile: ProfileOutputDTO


class UpdateAvatarInputDTO(DTO):
    profile_id: UUID
    # JSON patches are validated against the complete domain value after merging.
    changes: dict[str, JsonValue]


class AvatarSettingsOutputDTO(DTO):
    settings: AvatarSettings


class RenderedWidgetDTO(DTO):
    fill_color: str | None
    image: MediaOutputDTO | None


class AvatarOutputDTO(DTO):
    wrapper_shape: str
    background: Background
    gender: str
    widgets: dict[str, RenderedWidgetDTO]
