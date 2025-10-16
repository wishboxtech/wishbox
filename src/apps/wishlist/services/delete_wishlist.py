from src.apps.wishlist.selectors import delete_wishlist_by_id


def delete_wishlist(wishlist_id):
    deleted = delete_wishlist_by_id(id=wishlist_id)
    return deleted
