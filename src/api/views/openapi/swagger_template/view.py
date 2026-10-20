from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView


class SwaggerUIView(TemplateView):
    template_name = "swagger.html"

    # Getting the swagger/redoc yaml file as context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["schema_url"] = "openapi-schema-yaml"
        return context


# Caching the view for 15 minutes
swagger_ui_view = cache_page(60 * 15)(SwaggerUIView.as_view())
