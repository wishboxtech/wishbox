from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.permissions import IsOwnerOfWishlist
from src.apps.wishlist.services import delete_wishlist
from src.static import ErrorEnum
from src.utils.exceptions import NotFoundException


class DeleteWishlistAPIView(APIView):
    permission_classes = [IsOwnerOfWishlist]

    def delete(self, *args, **kwargs):
        wishlist_id = kwargs.get("id")
        profile_id = self.request.user.id

        obj = {"profile_id": profile_id, "wishlist_id": wishlist_id}
        self.check_object_permissions(self.request, obj)

        deleted = delete_wishlist(wishlist_id)
        if not deleted:
            raise NotFoundException(
                error_type=[ErrorEnum.Wishlist.WISHLIST_NOT_FOUND],
                message={"error": _("wishlist does not exist")},
            )

        return Response(
            data={
                "deleted": deleted,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
