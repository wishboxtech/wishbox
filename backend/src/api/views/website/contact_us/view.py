from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.website.dto import ListContactsInputDTO
from src.core.composition import website_service
from src.shared.domain.errors import NotFound

from src.api.views.website.contact_us.serializer import ContactOutputSerializer


class GetContactUsAPIView(APIView):
    # This endpoint uses the configured default permission policy.

    def get(self, request):
        try:
            result = website_service().list_contacts(ListContactsInputDTO())
        except NotFound as error:
            return Response({"detail": str(error)}, status=404)
        return Response(ContactOutputSerializer(result, many=True).data)
