from typing import Protocol
from uuid import UUID

from src.apps.authentication.dto import UserOutputDTO
from src.apps.profile.domain import Profile
from src.apps.profile.domain.avatar import AvatarSettings
from src.apps.profile.dto import UpsertProfileInputDTO
from src.shared.dto import IdInputDTO


class ProfileRepository(Protocol):
    def get(self, id: UUID) -> Profile | None:
        ...

    def exists(self, id: UUID) -> bool:
        ...

    def upsert(self, dto: UpsertProfileInputDTO) -> tuple[Profile, bool]:
        ...

    def get_avatar(self, id: UUID, *, lock: bool = False) -> AvatarSettings | None:
        ...

    def save_avatar(self, id: UUID, settings: AvatarSettings) -> None:
        ...

    def widget_media_ids(self, ids: tuple[UUID, ...]) -> dict[UUID, UUID]:
        ...


class AuthenticationServiceProtocol(Protocol):
    """AuthenticationService capabilities required by ProfileService."""

    def get_user(self, dto: IdInputDTO) -> UserOutputDTO | None:
        ...
