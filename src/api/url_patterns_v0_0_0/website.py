from django.urls import path

from src.api.views.website.contact_us import GetContactUsAPIView

website_urlpatterns = [
    path(
        "contact-us/",
        GetContactUsAPIView.as_view(),
        name="contact_us",
    )
]
