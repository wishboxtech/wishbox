from rest_framework.response import Response

from src.shared.domain.errors import DomainValidationError
from src.static import ErrorEnum

ERROR_CODES = {
    "wishlist_not_found": ErrorEnum.Wishlist.WISHLIST_NOT_FOUND,
    "wish_not_found": ErrorEnum.Wishlist.WISH_NOT_FOUND,
    "not_wishlist_owner": ErrorEnum.Wishlist.NOT_WISHLIST_OWNER,
    "avatar_not_found": ErrorEnum.Profile.AVATAR_NOT_FOUND,
    "invalid_avatar_settings": ErrorEnum.Profile.INVALID_AVATAR_SETTINGS,
    "invalid_otp": ErrorEnum.VerifyOneTimePassword.INAVLID_OTP,
    "otp_already_sent": ErrorEnum.SendOneTimePassword.OTP_ALREADY_SENT,
    "invalid_refresh": ErrorEnum.RefreshToken.TOKEN_IS_NOT_VALID,
    "invalid_user_id": ErrorEnum.Services.INVALID_USER_ID,
}


def domain_error_response(error, context):
    status = 403 if error.code == "not_wishlist_owner" else 400
    if isinstance(error, DomainValidationError):
        view = context.get("view")
        codes = getattr(view, "error_codes", {})
        errors = error.errors
        # Missing OTP target is a use-case rule, independent of input syntax.
        if type(view).__name__ == "SendOneTimePassword":
            codes = {
                "phone_number": ErrorEnum.SendOneTimePassword.PHONE_NUMBER_IS_EMPTY
            }
        error_types = [str(codes.get(field, field)) for field in errors]
    else:
        errors = {"error": str(error) or error.code}
        error_types = [ERROR_CODES.get(error.code, error.code)]
    return Response(
        {"ok": False, "data": errors, "status": status, "error_type": error_types},
        status=status,
    )
