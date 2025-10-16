from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.permissions import IsOwnerOfWishlist
from src.apps.wishlist.services import delete_wish
from src.static import ErrorEnum
from src.utils.exceptions import NotFoundException


class DeleteWishAPIView(APIView):
    permission_classes = [IsOwnerOfWishlist]

    def delete(self, *args, **kwargs):
        wishlist_id = kwargs.get("id")
        wish_id = kwargs.get("wishid")
        profile_id = self.request.user.id

        obj = {"profile_id": profile_id, "wishlist_id": wishlist_id}
        self.check_object_permissions(self.request, obj)

        deleted = delete_wish(wish_id)
        if not deleted:
            raise NotFoundException(
                error_type=[ErrorEnum.Wishlist.WISH_NOT_FOUND],
                message={"error": _("wish does not exist")},
            )

        return Response(
            data={
                "deleted": deleted,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
