from src.shared.domain.errors import DomainError


class InvalidOTP(DomainError):
    code = "invalid_otp"


class OTPAlreadySent(DomainError):
    code = "otp_already_sent"


class InvalidRefresh(DomainError):
    code = "invalid_refresh"


class InvalidUserID(DomainError):
    code = "invalid_user_id"
