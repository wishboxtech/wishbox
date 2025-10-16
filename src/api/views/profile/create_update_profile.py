from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.profile.services import create_or_update_profile
from src.utils.exceptions import BadRequestException


class CreateUpdateProfile(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, *args, **kwargs):
        user_id = self.request.user.id
        data = self.request.data
        data["profile"] = user_id
        created, profile, errs = create_or_update_profile(user_id=user_id, data=data)
        if errs:
            raise BadRequestException(
                message=errs.get("errors"),
                error_type=errs.get("error_type"),
            )
        return Response(
            data={
                "created": created,
                "data": profile,
                "status": status.HTTP_202_ACCEPTED,
            },
            status=status.HTTP_202_ACCEPTED,
        )
