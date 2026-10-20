from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True)
class Profile:
    profile_id: UUID
    first_name: str | None
    last_name: str | None
    birthdate: date | None
    gender: str | None
    bio: str | None
    photo_id: UUID | None
    cat_avatar: dict | None = None

    @property
    def registration_state(self) -> str:
        return "sign_in" if self.gender and self.birthdate else "sign_up"
