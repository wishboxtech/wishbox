from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from src.utils.exceptions import NotFoundException, BadRequestException, Unauthorized
from rest_framework.exceptions import NotAuthenticated
from src.static import ErrorEnum

def api_exception_handler(exc, context):
    """
    Custom exception handler for handling project-specific exceptions
    """
    if isinstance(exc, NotFoundException):
        return Response(
            {"detail": exc.message, "error_type": exc.error_type},
            status=status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, BadRequestException):
        return Response(
            {"detail": exc.message, "error_type": exc.error_type},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(exc, NotAuthenticated):
        return Response(
            data={
                "ok": False,
                "data": {"error": str(exc)},
                "status": status.HTTP_401_UNAUTHORIZED,
                "error_type": [ErrorEnum.Authentication.UNAUTHORIZED],
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if isinstance(exc, Unauthorized):
        return Response(
            {"detail": exc.message},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # Default response for unhandled exceptions
    return Response(
        {"detail": "An unexpected error occurred"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
