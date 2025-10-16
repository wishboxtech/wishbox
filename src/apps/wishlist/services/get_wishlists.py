from src.apps.wishlist.selectors import \
    get_wishlist_by_id as get_wishlist_by_id_selector
from src.apps.wishlist.selectors import \
    get_wishlists_by_profile as get_wishlists_by_profile_selector
from src.apps.wishlist.serializers import WishlistSerializer


def get_wishlists_by_profile(profile_id):
    """
    Return serialized wishlist data for a given profile_id.
    Returns Empty if no wishlists exists.
    """
    wishlists = get_wishlists_by_profile_selector(profile_id=profile_id)
    return WishlistSerializer(instance=wishlists, many=True).data


def get_wishlist_by_id(id):
    """
    Return serialized wishlist data for a given wishlist id.
    Returns None if no wishlists exists.
    """
    wishlist = get_wishlist_by_id_selector(id=id)
    if not wishlist:
        return None
    return WishlistSerializer(instance=wishlist).data
