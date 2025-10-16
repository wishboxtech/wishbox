from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.website.models import ContactUs
from src.apps.website.serializers import ContactUsSerializer
from src.utils.exceptions import NotFoundException


class GetContactUsAPIView(APIView):
    def get(self, request):
        try:
            contact_us = ContactUs.objects.all()
            if not contact_us.exists():
                raise NotFoundException(
                    "ContactUs instance not found", error_type="not_found"
                )
            serializer = ContactUsSerializer(contact_us, many=True)
            return Response(serializer.data)
        except NotFoundException as e:
            return Response({"detail": str(e)}, status=404)
