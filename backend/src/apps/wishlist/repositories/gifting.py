from django.db.models import Count, Q
from django.utils import timezone
from src.apps.wishlist.models import (
    AnonymousFriend,
    GuestIdentity,
    Notification,
    ReservationRequest,
    Wish,
    WishInteraction,
)
from src.apps.wishlist.repositories.wishlist import DjangoWishlistRepository
from src.apps.wishlist.dto.gifting import (
    ActivityOutputDTO,
    GiftRecordOutputDTO,
    GiftOutputDTO,
    InboxOutputDTO,
    NotificationOutputDTO,
)

ACTIVE = ("reserved", "purchased", "received")


def record(item):
    return GiftRecordOutputDTO(
        id=item.id,
        wish_id=item.wish_id,
        wishlist_id=item.wish.wishlist_id,
        owner_id=item.wish.wishlist.profile_id,
        friend_id=item.friend_id
        or (item.guest_identity.claimed_user_id if item.guest_identity_id else None),
        management_hash=""
        if item.guest_identity_id and item.guest_identity.consumed_at
        else item.management_hash,
        status=item.status,
        wish_name=item.wish.name,
        created_at=item.created_at,
        **{
            field: getattr(item, field)
            for field in (
                "purchase_by",
                "purchase_plan",
                "details_checked",
                "expires_at",
                "reminder_at",
                "reminded_at",
                "extension_count",
                "received_at",
                "fit",
                "private_note",
                "thank_you",
                "thank_you_sent_at",
                "follow_up_note",
                "follow_up_sent_at",
                "follow_up_acknowledged_at",
            )
        },
    )


def gift_output(item):
    # An explicit allowlist keeps recipient-only feedback out of giver responses.
    return GiftOutputDTO(
        **{
            name: getattr(item, name)
            for name in GiftOutputDTO.model_fields
            if name != "management_token"
        }
    )


class DjangoGiftRepository:
    def __init__(self, wishlists: DjangoWishlistRepository):
        self.wishlists = wishlists

    def wish(self, id, *, lock=False):
        return self.wishlists.get_wish(id, lock=lock)

    def wishlist(self, id):
        return self.wishlists.get_wishlist(id)

    def active(self, wish_id):
        item = (
            ReservationRequest.objects.select_related(
                "wish__wishlist", "guest_identity"
            )
            .filter(wish_id=wish_id, status__in=ACTIVE)
            .first()
        )
        return record(item) if item else None

    def activities(self, wish_ids, visitor, profile_id):
        now = timezone.now()
        rows = (
            Wish.objects.filter(id__in=wish_ids)
            .select_related("wishlist")
            .annotate(
                view_count=Count("interactions", filter=Q(interactions__viewed=True)),
                like_count=Count("interactions", filter=Q(interactions__liked=True)),
            )
        )
        liked = set(
            WishInteraction.objects.filter(
                wish_id__in=wish_ids, visitor=visitor, liked=True
            ).values_list("wish_id", flat=True)
        )
        gifts = {
            item.wish_id: item
            for item in ReservationRequest.objects.select_related("guest_identity")
            .filter(wish_id__in=wish_ids, status__in=ACTIVE)
            .exclude(status="reserved", expires_at__lte=now)
        }
        result = []
        for item in rows:
            gift = gifts.get(item.id)
            giver_id = (
                (
                    gift.friend_id
                    or (
                        gift.guest_identity.claimed_user_id
                        if gift.guest_identity_id
                        else None
                    )
                )
                if gift
                else None
            )
            result.append(
                ActivityOutputDTO(
                    wish_id=item.id,
                    views=item.view_count,
                    likes=item.like_count,
                    liked=item.id in liked,
                    status=gift.status if gift else "available",
                    is_owner=item.wishlist.profile_id == profile_id,
                    is_giver=bool(gift and profile_id and giver_id == profile_id),
                    reservation_id=gift.id
                    if gift
                    and profile_id
                    and (
                        giver_id == profile_id or item.wishlist.profile_id == profile_id
                    )
                    else None,
                )
            )
        return tuple(result)

    def interact(self, wish_id, visitor, action):
        item, _ = WishInteraction.objects.get_or_create(
            wish_id=wish_id, visitor=visitor
        )
        if action == "view":
            item.viewed = True
            item.save(update_fields=["viewed"])
        else:
            item.liked = action == "like"
            item.save(update_fields=["liked"])

    def reserve(self, wish, dto, token_hash, expires_at, reminder_at, guest_hash=""):
        profile_id, nickname = dto.profile_id, dto.nickname
        guest = (
            AnonymousFriend.objects.create(nickname=nickname)
            if profile_id is None
            else None
        )
        identity = None
        if guest_hash and profile_id is None:
            identity, _ = GuestIdentity.objects.get_or_create(key_hash=guest_hash)
            identity = GuestIdentity.objects.select_for_update().get(pk=identity.pk)
            if identity.consumed_at is not None:
                identity = None
        item = ReservationRequest.objects.create(
            wish_id=wish.id,
            friend_id=profile_id,
            anonymous_friend=guest,
            guest_identity=identity,
            status="reserved",
            management_hash=token_hash,
            purchase_by=dto.purchase_by,
            purchase_plan=dto.purchase_plan,
            details_checked=dto.details_checked,
            expires_at=expires_at,
            reminder_at=reminder_at,
        )
        Wish.objects.filter(id=wish.id).update(accepted_request=item)
        return record(
            ReservationRequest.objects.select_related(
                "wish__wishlist", "guest_identity"
            ).get(id=item.id)
        )

    def change(self, id, status, now):
        fields = {"status": status}
        if status == "received":
            fields["received_at"] = now
        ReservationRequest.objects.filter(id=id).update(**fields)
        item = ReservationRequest.objects.select_related(
            "wish__wishlist", "guest_identity"
        ).get(id=id)
        if status in ("cancelled", "expired"):
            Wish.objects.filter(id=item.wish_id).update(accepted_request=None)
        return record(item)

    def notify(self, profile_id, wish, event):
        Notification.objects.create(
            profile_id=profile_id, wish_id=wish.id, wish_name=wish.name, event=event
        )

    def gifts(self, profile_id):
        items = (
            ReservationRequest.objects.select_related(
                "wish__wishlist", "guest_identity"
            )
            .filter(
                Q(friend_id=profile_id) | Q(guest_identity__claimed_user_id=profile_id),
                wish__isnull=False,
            )
            .exclude(status__in=["pending", "accepted", "rejected"])
            .order_by("-created_at")[:200]
        )
        return tuple(gift_output(record(item)) for item in items)

    def inbox(self, profile_id):
        items = Notification.objects.filter(profile_id=profile_id)
        return InboxOutputDTO(
            unread=items.filter(read_at__isnull=True).count(),
            items=tuple(
                NotificationOutputDTO(
                    id=item.id,
                    wish_id=item.wish_id,
                    wish_name=item.wish_name,
                    event=item.event,
                    read_at=item.read_at,
                    created_at=item.created_at,
                )
                for item in items.order_by("-created_at", "-id")[:100]
            ),
        )

    def read(self, profile_id, notification_id):
        items = Notification.objects.filter(profile_id=profile_id, read_at__isnull=True)
        if notification_id is not None:
            items = items.filter(id=notification_id)
        items.update(read_at=timezone.now())

    def get_gift(self, id):
        item = (
            ReservationRequest.objects.select_related(
                "wish__wishlist", "guest_identity"
            )
            .filter(id=id, wish__isnull=False)
            .first()
        )
        return record(item) if item else None

    def reschedule(self, id, purchase_by, expires_at, reminder_at):
        from django.db.models import F

        ReservationRequest.objects.filter(id=id).update(
            purchase_by=purchase_by,
            expires_at=expires_at,
            reminder_at=reminder_at,
            reminded_at=None,
            extension_count=F("extension_count") + 1,
        )
        return self.get_gift(id)

    def candidates(self, now, *, wish_ids=None, wishlist_id=None, reminders=False):
        due = Q(expires_at__lte=now)
        if reminders:
            due |= Q(reminder_at__lte=now, reminded_at__isnull=True)
        items = ReservationRequest.objects.filter(
            due, status="reserved", wish__isnull=False
        )
        if wish_ids is not None:
            items = items.filter(wish_id__in=wish_ids)
        if wishlist_id is not None:
            items = items.filter(wish__wishlist_id=wishlist_id)
        return tuple(
            items.order_by("expires_at", "id").values_list("wish_id", flat=True)[:200]
        )

    def mark_reminded(self, id, now):
        ReservationRequest.objects.filter(id=id).update(reminded_at=now)

    def save_experience(self, dto, now):
        fields = {}
        if dto.action == "save_private":
            if "fit" in dto.model_fields_set:
                fields["fit"] = dto.fit or ""
            if "private_note" in dto.model_fields_set:
                fields["private_note"] = dto.private_note
        elif dto.action == "share_thanks":
            fields = {"thank_you": dto.thank_you, "thank_you_sent_at": now}
        elif dto.action == "withdraw_thanks":
            fields = {"thank_you": "", "thank_you_sent_at": None}
        elif dto.action == "share_follow_up":
            fields = {
                "follow_up_note": dto.follow_up_note,
                "follow_up_sent_at": now,
                "follow_up_acknowledged_at": None,
            }
        elif dto.action == "withdraw_follow_up":
            fields = {
                "follow_up_note": "",
                "follow_up_sent_at": None,
                "follow_up_acknowledged_at": None,
            }
        elif dto.action == "acknowledge_follow_up":
            fields = {"follow_up_acknowledged_at": now}
        if fields:
            ReservationRequest.objects.filter(id=dto.reservation_id).update(**fields)
        return self.get_gift(dto.reservation_id)
