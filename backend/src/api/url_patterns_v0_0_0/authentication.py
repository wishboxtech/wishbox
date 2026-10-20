from django.urls import path

from src.api.views.authentication.refresh_token.view import RefreshTokenAPIView
from src.api.views.authentication.send_otp.view import SendOneTimePassword
from src.api.views.authentication.verify_token.view import VerifyOneTimePasswordAPIView

authentication_urlpatterns = [
    path(
        "otp/",
        SendOneTimePassword.as_view(),
        name="send_otp",
    ),
    path("otp/verify/", VerifyOneTimePasswordAPIView.as_view(), name="verify_otp"),
    path("otp/refresh/", RefreshTokenAPIView.as_view(), name="refresh_token"),
]
