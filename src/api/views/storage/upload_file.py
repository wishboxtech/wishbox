from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from src.apps.storage.services import create_media
from src.static import ErrorEnum
from src.utils.exceptions import BadRequestException


class UploadFile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        file = self.request.data.get("file")
        if file is None:
            raise BadRequestException(
                message={"error": _("file must not be empty")},
                error_type=[ErrorEnum.UploadFile.FILE_IS_EMPTY],
            )
        media_id = create_media(media=file)
        return Response(
            data={
                "ok": True,
                "data": {"media_id": media_id},
                "status": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
        )
