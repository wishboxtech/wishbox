from rest_framework.permissions import IsAuthenticated

from src.apps.wishlist.selectors import is_owner_of_wishlist


class IsOwnerOfWishlist(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        res = is_owner_of_wishlist(
            id=obj.get("wishlist_id"),
            profile_id=obj.get("profile_id"),
        )
        return super().has_permission(request, view) and res
