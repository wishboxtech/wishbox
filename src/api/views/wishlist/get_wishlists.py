from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.wishlist.services import get_wishlists_by_profile


class GetWishlistsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        user_id = self.request.user.id
        wishlists = get_wishlists_by_profile(profile_id=user_id)
        return Response(
            data={
                "ok": True,
                "data": wishlists,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )
