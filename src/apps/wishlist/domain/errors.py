from src.shared.domain.errors import DomainError, NotFound


class WishlistNotFound(NotFound):
    code = "wishlist_not_found"


class WishNotFound(NotFound):
    code = "wish_not_found"


class NotWishlistOwner(DomainError):
    code = "not_wishlist_owner"
