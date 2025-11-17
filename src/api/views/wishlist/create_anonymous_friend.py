from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.wishlist.services import create_anonymous_friend
from src.utils.exceptions import BadRequestException


class CreateAnonymousFriendAPIView(APIView):
    permission_classes = []

    def post(self, *args, **kwargs):
        created, anonymous_friend_id, errs = create_anonymous_friend(
            data=self.request.data
        )

        if errs:
            raise BadRequestException(
                message=errs.get("errors"),
                error_type=errs.get("error_type"),
            )
        return Response(
            data={
                "created": created,
                "anonymous_friend_id": anonymous_friend_id,
                "status": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
        )
