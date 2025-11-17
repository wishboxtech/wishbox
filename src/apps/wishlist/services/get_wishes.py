from src.apps.wishlist.selectors import get_wish_by_id as get_wish_by_id_selector
from src.apps.wishlist.selectors import get_wishes_by_wishlist_id as get_wishes_selector
from src.apps.wishlist.serializers import WishSerializer


def get_wishes_by_wishlist_id(wishlist_id):
    """
    Return serialized wishes data for a given wishlist_id.
    Returns Empty if no wishes exists.
    """
    wishlists = get_wishes_selector(wishlist_id=wishlist_id)
    return WishSerializer(instance=wishlists, many=True).data


def get_wish_by_id(id):
    """
    Return serialized wish data for a given wish id.
    Returns None if no wish exists.
    """
    wishlist = get_wish_by_id_selector(id=id)
    if not wishlist:
        return None
    return WishSerializer(instance=wishlist).data
