from django.urls import path
from src.api.views.wallet.create_card import CreateCardAPIView

wallet_urlpatterns = [
    path(
        "card/",
        CreateCardAPIView.as_view(),
        name="card",
    ),
]
