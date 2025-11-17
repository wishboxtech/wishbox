from django.urls import include, path

from settings import ENABLE_SWAGGER
from src.api.url_patterns_v0_0_0.authentication import authentication_urlpatterns
from src.api.url_patterns_v0_0_0.openapi import openapi_urlpatterns
from src.api.url_patterns_v0_0_0.profile import profile_urlpatterns
from src.api.url_patterns_v0_0_0.storage import storage_urlpatterns
from src.api.url_patterns_v0_0_0.website import website_urlpatterns
from src.api.url_patterns_v0_0_0.wish import wish_urlpatterns
from src.api.url_patterns_v0_0_0.wishlist import wishlist_urlpatterns

V_0_0_0_url_patterns = [
    path("website/", include(website_urlpatterns)),
    path("auth/", include(authentication_urlpatterns)),
    path("profile/", include(profile_urlpatterns)),
    path("wishlist/", include(wishlist_urlpatterns)),
    path("storage/", include(storage_urlpatterns)),
    path("wish/", include(wish_urlpatterns)),
]


V_0_0_0_url_patterns += [
    path("openapi/", include(openapi_urlpatterns)),
]


urlpatterns = [
    path("V0.0.0/", include(V_0_0_0_url_patterns)),
]
