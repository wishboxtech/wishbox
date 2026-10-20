from uuid import UUID

from src.shared.domain.errors import DomainValidationError


def require_reservation_actor(
    friend: UUID | None, anonymous_friend: UUID | None
) -> None:
    if friend is None and anonymous_friend is None:
        raise DomainValidationError(
            {
                "friend": "A friend or anonymous friend is required.",
                "anonymous_friend": "A friend or anonymous friend is required.",
            }
        )
