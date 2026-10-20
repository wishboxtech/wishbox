from typing import Protocol
from uuid import UUID

from src.apps.authentication.domain import User
from src.apps.authentication.dto import (
    CreateUserInputDTO,
    TokensOutputDTO,
    VerifiedOTPOutputDTO,
    VerifyOTPInputDTO,
)


class GuestClaims(Protocol):
    def claim(self, key: str, user_id: UUID) -> bool:
        ...


class UserRepository(Protocol):
    def get(self, id: UUID) -> User | None:
        ...

    def find(self, identifier: str) -> User | None:
        ...

    def create(self, dto: CreateUserInputDTO) -> User:
        ...


class OTPRepository(Protocol):
    def exists(self, target: str, prefix: str) -> bool:
        ...

    def create(self, target: str, state: str, prefix: str) -> tuple[str, str]:
        ...

    def verify(self, dto: VerifyOTPInputDTO) -> VerifiedOTPOutputDTO:
        ...


class TokenIssuer(Protocol):
    def issue(self, user_id: UUID) -> TokensOutputDTO:
        ...

    def refresh(self, token: str) -> TokensOutputDTO:
        ...


class OTPNotifier(Protocol):
    def __call__(self, phone: str, code: str) -> None:
        ...
