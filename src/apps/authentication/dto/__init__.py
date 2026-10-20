from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field

from src.shared.dto import DTO


class SendOTPInputDTO(DTO):
    phone_number: Annotated[str, Field(pattern=r"^09\d{9}$")] | None = None
    email: str | None = None
    prefix: str = ""


class SendOTPOutputDTO(DTO):
    otp_id: str


class VerifyOTPInputDTO(DTO):
    otp_id: str
    otp_code: str
    prefix: str = ""


class VerifiedOTPOutputDTO(DTO):
    identifier: str
    state: Literal["phone_number", "email"]


class CreateUserInputDTO(DTO):
    phone_number: Annotated[str, Field(pattern=r"^09\d{9}$")] | None = None
    email: str | None = None
    password: str | None = None


class UserOutputDTO(DTO):
    id: UUID
    phone_number: str | None
    email: str | None
    is_active: bool
    is_phone_number_verified: bool
    has_accepted_terms: bool


class IdentifierInputDTO(DTO):
    identifier: str


class RefreshInputDTO(DTO):
    token: str


class TokensOutputDTO(DTO):
    access_token: str
    refresh_token: str
