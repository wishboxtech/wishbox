from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.storage.dto import UploadMediaInputDTO
from src.core.composition import storage_service
from src.static import ErrorEnum
from src.utils.exceptions import BadRequestException


from src.api.views.storage.upload_file.serializer import (
    UploadMediaInputSerializer,
    UploadMediaOutputSerializer,
)


class UploadFile(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        serializer = UploadMediaInputSerializer(data=self.request.data)
        if not serializer.is_valid():
            raise BadRequestException(
                serializer.errors, [ErrorEnum.UploadFile.FILE_IS_EMPTY]
            )
        file = serializer.validated_data["file"]
        dto = UploadMediaInputDTO(filename=file.name, content=file.read())
        result = storage_service().upload(dto)
        return Response(
            {
                "ok": True,
                "data": UploadMediaOutputSerializer(result).data,
                "status": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
        )
