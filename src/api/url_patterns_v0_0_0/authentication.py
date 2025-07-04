from django.urls import path
from src.api.views.authentication import (
    SendOneTimePassword, 
    VerifyOneTimePasswordAPIView,
    RefreshTokenAPIView,
    )

authentication_urlpatterns = [
    path(
        "otp/",
        SendOneTimePassword.as_view(),
        name="send_otp",
    ),
    path(
        "otp/verify/",
        VerifyOneTimePasswordAPIView.as_view(),
        name="verify_otp"
    ),
    path(
        "otp/refresh/",
        RefreshTokenAPIView.as_view(),
        name="refresh_token"
    )
]
