from src.api.views.profile.get_profile import GetProfileAPIView
from src.api.views.profile.create_update_profile import CreateUpdateProfile
from src.api.views.profile.create_wishlist import CreateWishlist
from src.api.views.profile.update_wishlist import UpdateWishlist
from src.api.views.profile.get_wishlists import GetWishlistsAPIView


class WishlistAPIView(GetWishlistsAPIView, CreateWishlist):
    pass


class ProfileAPIView(CreateUpdateProfile, GetProfileAPIView):
    pass
