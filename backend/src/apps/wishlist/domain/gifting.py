from src.shared.domain.errors import DomainError


class GiftNotFound(DomainError):
    code = "gift_not_found"


class GiftConflict(DomainError):
    code = "gift_conflict"


class GiftForbidden(DomainError):
    code = "gift_forbidden"


def next_gift_status(current: str, action: str, *, owner: bool, giver: bool) -> str:
    if action == "receive":
        if not owner:
            raise GiftForbidden("Only the wishlist owner can confirm receipt.")
        if current != "purchased":
            raise GiftConflict("The giver needs to mark this gift as purchased first.")
        return "received"
    if not giver:
        raise GiftForbidden("Only the person who reserved this gift can change it.")
    if action == "purchase" and current == "reserved":
        return "purchased"
    if action == "cancel" and current in ("reserved", "purchased"):
        return "cancelled"
    raise GiftConflict(
        "This gift has already moved to another stage. Refresh and try again."
    )
