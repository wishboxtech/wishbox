from src.apps.wishlist.domain import Wish as WishEntity
from src.apps.wishlist.domain import Wishlist as WishlistEntity
from src.apps.wishlist.dto import AnonymousFriendOutputDTO, ReservationOutputDTO
from src.apps.wishlist.models import AnonymousFriend, ReservationRequest, Wish, Wishlist


def wishlist_entity(item):
    return WishlistEntity(
        id=item.id,
        profile_id=item.profile_id,
        name=item.name,
        description=item.description,
        cover_id=item.cover_id,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


def wish_entity(item):
    return WishEntity(
        id=item.id,
        wishlist_id=item.wishlist_id,
        name=item.name,
        description=item.description,
        price=item.price,
        cover_id=item.cover_id,
        accepted_request_id=item.accepted_request_id,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


class DjangoWishlistRepository:
    def get_wishlist(self, id, *, lock=False):
        query = Wishlist.objects.all()
        if lock:
            query = query.select_for_update()
        item = query.filter(id=id).first()
        return wishlist_entity(item) if item else None

    def list_wishlists(self, profile_id):
        return tuple(
            wishlist_entity(item)
            for item in Wishlist.objects.filter(profile_id=profile_id).order_by(
                "created_at", "id"
            )
        )

    def create_wishlist(self, dto):
        return wishlist_entity(Wishlist.objects.create(**dto.model_dump()))

    def update_wishlist(self, dto):
        item = Wishlist.objects.get(id=dto.id)
        fields = dto.model_dump(exclude_unset=True, exclude={"id", "profile_id"})
        for key, value in fields.items():
            setattr(item, key, value)
        item.save()
        return wishlist_entity(item)

    def delete_wishlist(self, id):
        count, _ = Wishlist.objects.filter(id=id).delete()
        return count > 0

    def get_wish(self, id, *, lock=False):
        query = Wish.objects.all()
        if lock:
            query = query.select_for_update()
        item = query.filter(id=id).first()
        return wish_entity(item) if item else None

    def list_wishes(self, wishlist_id):
        return tuple(
            wish_entity(item)
            for item in Wish.objects.filter(wishlist_id=wishlist_id).order_by(
                "created_at", "id"
            )
        )

    def create_wish(self, dto):
        fields = dto.model_dump(exclude={"profile_id"})
        return wish_entity(Wish.objects.create(**fields))

    def update_wish(self, dto):
        item = Wish.objects.get(id=dto.id)
        fields = dto.model_dump(
            exclude_unset=True, exclude={"id", "profile_id", "wishlist_id"}
        )
        for key, value in fields.items():
            setattr(item, key, value)
        item.save()
        return wish_entity(item)

    def delete_wish(self, id):
        count, _ = Wish.objects.filter(id=id).delete()
        return count > 0

    def create_anonymous_friend(self, dto):
        item = AnonymousFriend.objects.create(nickname=dto.nickname)
        return AnonymousFriendOutputDTO(id=item.id)

    def anonymous_friend_exists(self, id):
        return AnonymousFriend.objects.filter(id=id).exists()

    def create_reservation(self, dto):
        item = ReservationRequest.objects.create(**dto.model_dump())
        return ReservationOutputDTO(
            wish=item.wish_id,
            friend=item.friend_id,
            anonymous_friend=item.anonymous_friend_id,
            status=item.status,
            created_at=item.created_at,
        )
