import uuid
from typing import Union

from django.db.models import BooleanField, Case, Q, Value, When

from src.apps.wishlist.models import Wish


def get_wishes_by_wishlist_id(wishlist_id: Union[str, uuid.UUID]):
    return Wish.objects.only(
        "id",
        "name",
        "description",
        "price",
        "cover",
    ).filter(wishlist_id=wishlist_id)


def get_wish_by_id(id: Union[str, uuid.UUID]):
    try:
        return (
            Wish.objects.select_related("accepted_request")
            .only(
                "id",
                "name",
                "description",
                "cover",
                "accepted_request",
            )
            .annotate(
                reserved=Case(
                    When(Q(accepted_request__isnull=False), then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
            .get(id=id)
        )
    except Wish.DoesNotExist:
        return None
