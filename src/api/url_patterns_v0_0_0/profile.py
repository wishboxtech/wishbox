from django.urls import path
from src.api.views.profile import ProfileAPIView

profile_urlpatterns = [
    path(
        "",
        ProfileAPIView.as_view(),
        name="profile",
    ),
]