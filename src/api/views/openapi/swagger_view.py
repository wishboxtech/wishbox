from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import cache_page


# Caching for 15 minutes
@cache_page(60 * 15)
def swagger_schema_view(request):
    # Reading the yaml file and returning it.
    base_dir = Path(settings.BASE_DIR)
    with open(base_dir / "openapi" / "swagger.yaml", "r") as file:
        schema = file.read()
    return HttpResponse(schema, content_type="text/yaml")
