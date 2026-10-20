from src.shared.domain.errors import DomainError, NotFound


class AvatarNotFound(NotFound):
    code = "avatar_not_found"


class InvalidAvatarSettings(DomainError):
    code = "invalid_avatar_settings"
