from src.apps.wishlist.models import Wishlist


def is_owner_of_wishlist(id, profile_id):
    return Wishlist.objects.filter(id=id, profile_id=profile_id)
