from django.urls import include, path
from src.api.url_patterns_v0_0_0.website import website_urlpatterns
from src.api.url_patterns_v0_0_0.openapi import openapi_urlpatterns
from src.api.url_patterns_v0_0_0.authentication import authentication_urlpatterns
from settings import ENABLE_SWAGGER

V_0_0_0_url_patterns = [
    path("website/", include(website_urlpatterns)),
    path("auth/", include(authentication_urlpatterns)),
]

if ENABLE_SWAGGER:
    V_0_0_0_url_patterns += [
        path("openapi/", include(openapi_urlpatterns)),
    ]


urlpatterns = [
    path("V0.0.0/", include(V_0_0_0_url_patterns)),
]
