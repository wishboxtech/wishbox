from django.urls import path
from src.api.views.openapi import swagger_schema_view, swagger_ui_view

openapi_urlpatterns = [
    path(
        "",
        swagger_ui_view,
        name="swagger-ui",
    ),
    path(
        "schema.yaml",
        swagger_schema_view,
        name="openapi-schema-yaml",
    ),
]
