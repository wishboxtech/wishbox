from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from src.apps.wallet.services import create_card
from src.utils.exceptions import BadRequestException, NotFoundException


class CreateCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user_id = self.request.user.id
        data = dict(self.request.data)
        data["user"] = user_id

        card, errs, done = create_card(data=data)

        if not done:
            raise BadRequestException(
                error_type=errs.get("error_type"),
                message=errs.get("message"),
            )

        return Response(
            data={
                "ok": True,
                "data": card,
                "status": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
        )
