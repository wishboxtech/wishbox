from django.urls import path

from src.api.views.openapi.swagger_template.view import swagger_ui_view
from src.api.views.openapi.swagger_view.view import swagger_schema_view

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
