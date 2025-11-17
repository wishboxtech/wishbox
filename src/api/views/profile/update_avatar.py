from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.profile.services import update_avatar
from src.utils.exceptions import BadRequestException


class UpdateAvatarAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, *args, **kwargs):
        user_id = self.request.user.id
        data = self.request.data
        try:
            data = update_avatar(profile_id=user_id, data=data)
        except Exception as e:
            raise BadRequestException(
                message=e.message,
                error_type=e.error_type,
            )

        return Response(
            data={
                "updated": True,
                "data": data,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
