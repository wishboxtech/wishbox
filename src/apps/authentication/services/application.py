from dataclasses import asdict

from src.apps.authentication.domain.errors import InvalidUserID, OTPAlreadySent
from src.apps.authentication.dto import (
    CreateUserInputDTO,
    IdentifierInputDTO,
    RefreshInputDTO,
    SendOTPInputDTO,
    SendOTPOutputDTO,
    TokensOutputDTO,
    UserOutputDTO,
    VerifiedOTPOutputDTO,
    VerifyOTPInputDTO,
)
from src.apps.authentication.interfaces import (
    OTPNotifier,
    OTPRepository,
    TokenIssuer,
    UserRepository,
)
from src.shared.domain.errors import DomainValidationError
from src.shared.dto import IdInputDTO
from src.shared.interfaces import AfterCommit, TransactionBoundary


class AuthenticationService:
    def __init__(
        self,
        users: UserRepository,
        otps: OTPRepository,
        tokens: TokenIssuer,
        notify: OTPNotifier,
        transaction: TransactionBoundary,
        after_commit: AfterCommit,
    ):
        self.users = users
        self.otps = otps
        self.tokens = tokens
        self.notify = notify
        self.transaction = transaction
        self.after_commit = after_commit

    def get_user(self, dto: IdInputDTO) -> UserOutputDTO | None:
        user = self.users.get(dto.id)
        return UserOutputDTO(**asdict(user)) if user else None

    def find_user(self, dto: IdentifierInputDTO) -> UserOutputDTO | None:
        user = self.users.find(dto.identifier)
        return UserOutputDTO(**asdict(user)) if user else None

    def create_user(self, dto: CreateUserInputDTO) -> UserOutputDTO:
        if not (dto.phone_number or dto.email):
            raise DomainValidationError(
                {"phone_number": "Phone number or email is required."}
            )
        with self.transaction():
            user = self.users.create(dto)
        return UserOutputDTO(**asdict(user))

    def send_otp(self, dto: SendOTPInputDTO) -> SendOTPOutputDTO:
        target = dto.phone_number or dto.email
        if not target:
            raise DomainValidationError(
                {"phone_number": "Phone number or email is required."}
            )
        if self.otps.exists(target, dto.prefix):
            raise OTPAlreadySent()
        state = "phone_number" if dto.phone_number else "email"
        otp_id, code = self.otps.create(target, state, dto.prefix)
        if dto.phone_number:
            self.after_commit(lambda: self.notify(dto.phone_number, code))
        return SendOTPOutputDTO(otp_id=otp_id)

    def verify_otp(self, dto: VerifyOTPInputDTO) -> VerifiedOTPOutputDTO:
        return self.otps.verify(dto)

    def verify_and_login(self, dto: VerifyOTPInputDTO) -> TokensOutputDTO:
        verified = self.otps.verify(dto)
        with self.transaction():
            user = self.users.find(verified.identifier)
            if user is None:
                fields = {verified.state: verified.identifier}
                user = self.users.create(CreateUserInputDTO(**fields))
        if not user.is_active:
            raise InvalidUserID()
        return self.tokens.issue(user.id)

    def login(self, dto: IdInputDTO) -> TokensOutputDTO:
        user = self.users.get(dto.id)
        if user is None or not user.is_active:
            raise InvalidUserID()
        return self.tokens.issue(user.id)

    def refresh(self, dto: RefreshInputDTO) -> TokensOutputDTO:
        return self.tokens.refresh(dto.token)
