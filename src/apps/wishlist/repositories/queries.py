from src.apps.wishlist.repositories.query_delete_wish import delete_wish_by_id
from src.apps.wishlist.repositories.query_delete_wishlist import delete_wishlist_by_id
from src.apps.wishlist.repositories.query_get_wishes import (
    get_wish_by_id,
    get_wishes_by_wishlist_id,
)
from src.apps.wishlist.repositories.query_get_wishlists import (
    get_wishlist_by_id,
    get_wishlists_by_profile,
)
from src.apps.wishlist.repositories.query_rules import is_owner_of_wishlist
