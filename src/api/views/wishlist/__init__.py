from rest_framework.permissions import AllowAny

from src.api.permissions import IsOwnerOfWishlist
from src.api.views.wishlist.create_wish import CreateWishAPIVIew
from src.api.views.wishlist.create_wishlist import CreateWishlistAPIView
from src.api.views.wishlist.get_wish_by_id import GetWishByIdAPIView
from src.api.views.wishlist.get_wishes import GetWishesAPIView
from src.api.views.wishlist.get_wishlists import GetWishlistsAPIView
from src.api.views.wishlist.update_wish import UpdateWishAPIView
from src.api.views.wishlist.update_wishlist import UpdateWishlistAPIView
from src.api.views.wishlist.delete_wish import DeleteWishAPIView
from src.api.views.wishlist.delete_wishlist import DeleteWishlistAPIView


class WishlistAPIView(GetWishlistsAPIView, CreateWishlistAPIView): ...


class WishActionAPIView(UpdateWishAPIView, DeleteWishAPIView): ...


class WishlistActionAPIView(
    GetWishesAPIView, CreateWishAPIVIew, UpdateWishlistAPIView, DeleteWishlistAPIView
):

    def check_object_permissions(self, request, obj):
        if self.request.method.lower() == "post":
            self.permission_classes = [IsOwnerOfWishlist]
        if self.request.method.lower() == "delete":
            self.permission_classes = [IsOwnerOfWishlist]
        if self.request.method.lower() == "patch":
            self.permission_classes = [IsOwnerOfWishlist]
        return super().check_object_permissions(request, obj)
