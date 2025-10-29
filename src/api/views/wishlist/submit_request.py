from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.wishlist.services import submit_request
from src.utils.exceptions import BadRequestException


class SubmitRequestAPIView(APIView):
    permission_classes = []

    def post(self, *args, **kwargs):
        wish_id = kwargs.get("id")

        data = self.request.data
        data["wish"] = wish_id
        created, reservation_data, errs = submit_request(data=data)

        if errs:
            raise BadRequestException(
                message=errs.get("errors"),
                error_type=errs.get("error_type"),
            )
        return Response(
            data={
                "created": created,
                "data": reservation_data,
                "status": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
        )