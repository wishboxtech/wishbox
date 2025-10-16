from src.apps.wishlist.selectors import delete_wish_by_id


def delete_wish(wish_id):
    deleted = delete_wish_by_id(id=wish_id)
    return deleted
