from django.urls import path
from src.api.views.authentication.send_otp import SendOneTimePassword

authentication_urlpatterns = [
    path(
        "otp/",
        SendOneTimePassword.as_view(),
        name="send_otp",
    ),
]
