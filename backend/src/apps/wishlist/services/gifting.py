from src.apps.wishlist.domain.commitment import (
    require_purchase_date,
    reservation_times,
    require_extension,
)
from src.apps.wishlist.domain.gifting import (
    GiftConflict,
    GiftForbidden,
    GiftNotFound,
    next_gift_status,
)
from src.apps.wishlist.dto import ListWishesInputDTO
from src.apps.wishlist.dto.gifting import (
    ActivityInputDTO,
    ReserveGiftInputDTO,
    ChangeGiftInputDTO,
    GiftOutputDTO,
    SharedListInputDTO,
    SharedListOutputDTO,
    InboxInputDTO,
    GiftExperienceInputDTO,
    SaveExperienceInputDTO,
    OwnerExperienceOutputDTO,
    OwnerGiftSummaryOutputDTO,
    GiverExperienceOutputDTO,
    MaintenanceOutputDTO,
)
from src.apps.wishlist.gifting_interfaces import (
    GiftRepository,
    GiftCredentials,
    WishlistReader,
    GiftClock,
)
from src.apps.wishlist.interfaces import ProfileServiceProtocol
from src.shared.dto import IdInputDTO
from src.shared.domain.errors import DomainValidationError
from src.shared.interfaces import TransactionBoundary


class GiftingService:
    def __init__(
        self,
        repository: GiftRepository,
        credentials: GiftCredentials,
        wishlists: WishlistReader,
        profiles: ProfileServiceProtocol,
        transaction: TransactionBoundary,
        clock: GiftClock,
    ):
        self.repository = repository
        self.credentials = credentials
        self.wishlists = wishlists
        self.profiles = profiles
        self.transaction = transaction
        self.clock = clock

    def _wish(self, id, *, lock=False):
        wish = self.repository.wish(id, lock=lock)
        if wish is None:
            raise GiftNotFound("This wish no longer exists.")
        return wish

    def _visitor(self, profile_id, visitor):
        return f"p:{profile_id}" if profile_id else f"v:{visitor}"

    def activity(self, dto: ActivityInputDTO):
        self.maintain(wish_ids=(dto.wish_id,))
        if dto.action:
            with self.transaction():
                self._wish(dto.wish_id, lock=True)
                self.repository.interact(
                    dto.wish_id, self._visitor(dto.profile_id, dto.visitor), dto.action
                )
        else:
            self._wish(dto.wish_id)
        result = self.repository.activities(
            (dto.wish_id,), self._visitor(dto.profile_id, dto.visitor), dto.profile_id
        )[0]
        if dto.token and not result.is_giver:
            gift = self.repository.active(dto.wish_id)
            if gift and self.credentials.matches(dto.token, gift.management_hash):
                result = result.model_copy(
                    update={"is_giver": True, "reservation_id": gift.id}
                )
        return result

    def shared_list(self, dto: SharedListInputDTO):
        self.maintain(wishlist_id=dto.wishlist_id)
        item = self.repository.wishlist(dto.wishlist_id)
        if item is None:
            raise GiftNotFound("This wishlist no longer exists.")
        wishes = self.wishlists.list_wishes(
            ListWishesInputDTO(wishlist_id=dto.wishlist_id)
        )
        return SharedListOutputDTO(
            wishlist=self.wishlists.get_wishlist(IdInputDTO(id=dto.wishlist_id)),
            wishes=wishes,
            activity=self.repository.activities(
                tuple(w.id for w in wishes),
                self._visitor(dto.profile_id, dto.visitor),
                dto.profile_id,
            ),
            is_owner=item.profile_id == dto.profile_id,
        )

    def reserve(self, dto: ReserveGiftInputDTO):
        now = self.clock()
        require_purchase_date(dto.purchase_by, now)
        if not dto.details_checked:
            raise DomainValidationError(
                {"details_checked": "Check the wish details before making a plan."}
            )
        expires_at, reminder_at = reservation_times(dto.purchase_by, now)
        token = self.credentials.issue()
        with self.transaction():
            wish = self._wish(dto.wish_id, lock=True)
            owner = self.repository.wishlist(wish.wishlist_id)
            if owner.profile_id == dto.profile_id:
                raise GiftForbidden("You cannot reserve your own wish.")
            if dto.profile_id and not self.profiles.exists(dto.profile_id):
                raise DomainValidationError(
                    {"profile": "Create your profile before reserving a gift."}
                )
            self._expire_locked(wish, now)
            if self.repository.active(wish.id):
                raise GiftConflict("Someone has already reserved this wish.")
            gift = self.repository.reserve(
                wish,
                dto,
                self.credentials.digest(token),
                expires_at,
                reminder_at,
                guest_hash=self.credentials.digest(dto.guest_key)
                if dto.guest_key and not dto.profile_id
                else "",
            )
            self.repository.notify(owner.profile_id, wish, "reserved")
        return self._output(gift, token)

    def change(self, dto: ChangeGiftInputDTO):
        self.maintain(wish_ids=(dto.wish_id,))
        now = self.clock()
        with self.transaction():
            wish = self._wish(dto.wish_id, lock=True)
            gift = self.repository.active(wish.id)
            if gift is None:
                raise GiftConflict("This wish has no active reservation.")
            now = self.clock()
            if gift.status == "reserved" and gift.expires_at and gift.expires_at <= now:
                raise GiftConflict(
                    "This hold has ended. Make a fresh plan if the wish is available."
                )
            giver = bool(
                dto.profile_id and gift.friend_id == dto.profile_id
            ) or self.credentials.matches(dto.token, gift.management_hash)
            if dto.action == "reschedule":
                if not giver:
                    raise GiftForbidden("Only the giver can change their plan.")
                require_extension(gift, dto.purchase_by, now)
                expires_at, reminder_at = reservation_times(dto.purchase_by, now)
                return self._output(
                    self.repository.reschedule(
                        gift.id, dto.purchase_by, expires_at, reminder_at
                    )
                )
            status = next_gift_status(
                gift.status,
                dto.action,
                owner=bool(dto.profile_id and gift.owner_id == dto.profile_id),
                giver=giver,
            )
            gift = self.repository.change(gift.id, status, now)
            self.repository.notify(gift.owner_id, wish, status)
            if (
                status == "received"
                and gift.friend_id
                and self.profiles.exists(gift.friend_id)
            ):
                self.repository.notify(gift.friend_id, wish, "gift_received")
        return self._output(gift, hide_plan=dto.action == "receive")

    def _output(self, gift, token=None, hide_plan=False):
        result = GiftOutputDTO(
            **{
                name: getattr(gift, name)
                for name in GiftOutputDTO.model_fields
                if name != "management_token"
            },
            management_token=token,
        )
        if hide_plan:
            result = result.model_copy(
                update={
                    "purchase_by": None,
                    "purchase_plan": "",
                    "expires_at": None,
                    "extension_count": 0,
                }
            )
        return result

    def gifts(self, dto: InboxInputDTO):
        self.maintain()
        return self.repository.gifts(dto.profile_id)

    def inbox(self, dto: InboxInputDTO):
        return self.repository.inbox(dto.profile_id)

    def read_notifications(self, dto: InboxInputDTO):
        with self.transaction():
            self.repository.read(dto.profile_id, dto.notification_id)
        return self.repository.inbox(dto.profile_id)

    def _expire_locked(self, wish, now):
        gift = self.repository.active(wish.id)
        if (
            gift
            and gift.status == "reserved"
            and gift.expires_at
            and gift.expires_at <= now
        ):
            self.repository.change(gift.id, "expired", now)
            self.repository.notify(gift.owner_id, wish, "hold_released")
            if gift.friend_id and self.profiles.exists(gift.friend_id):
                self.repository.notify(gift.friend_id, wish, "hold_expired")
            return True
        return False

    def maintain(self, *, wish_ids=None, wishlist_id=None, reminders=False):
        now = self.clock()
        expired = reminded = 0
        for wish_id in self.repository.candidates(
            now, wish_ids=wish_ids, wishlist_id=wishlist_id, reminders=reminders
        ):
            with self.transaction():
                wish = self.repository.wish(wish_id, lock=True)
                if wish is None:
                    continue
                if self._expire_locked(wish, now):
                    expired += 1
                    continue
                gift = self.repository.active(wish.id)
                if (
                    reminders
                    and gift
                    and gift.status == "reserved"
                    and gift.reminder_at
                    and gift.reminder_at <= now
                    and gift.reminded_at is None
                ):
                    self.repository.mark_reminded(gift.id, now)
                    if gift.friend_id and self.profiles.exists(gift.friend_id):
                        self.repository.notify(gift.friend_id, wish, "plan_reminder")
                    reminded += 1
        return MaintenanceOutputDTO(expired=expired, reminded=reminded)

    def _authorized_experience(self, dto):
        gift = self.repository.get_gift(dto.reservation_id)
        if gift is None:
            raise GiftNotFound("This gift no longer exists.")
        owner = bool(dto.profile_id and dto.profile_id == gift.owner_id)
        giver = bool(
            dto.profile_id and dto.profile_id == gift.friend_id
        ) or self.credentials.matches(dto.token, gift.management_hash)
        if not owner and not giver:
            # Do not reveal whether an arbitrary reservation ID exists.
            raise GiftNotFound("This gift no longer exists.")
        return gift, owner

    def _experience_output(self, gift, owner):
        if owner:
            return OwnerExperienceOutputDTO(
                gift=OwnerGiftSummaryOutputDTO(
                    id=gift.id,
                    wish_id=gift.wish_id,
                    wish_name=gift.wish_name,
                    status=gift.status,
                    received_at=gift.received_at,
                ),
                fit=gift.fit,
                private_note=gift.private_note,
                thank_you=gift.thank_you,
                thank_you_sent_at=gift.thank_you_sent_at,
                follow_up_note=gift.follow_up_note,
                follow_up_sent_at=gift.follow_up_sent_at,
                follow_up_acknowledged_at=gift.follow_up_acknowledged_at,
            )
        return GiverExperienceOutputDTO(gift=self._output(gift))

    def experience(self, dto: GiftExperienceInputDTO):
        gift, owner = self._authorized_experience(dto)
        self.maintain(wish_ids=(gift.wish_id,))
        gift, owner = self._authorized_experience(dto)
        return self._experience_output(gift, owner)

    def save_experience(self, dto: SaveExperienceInputDTO):
        gift, owner = self._authorized_experience(dto)
        if not owner and dto.action != "acknowledge_follow_up":
            raise GiftForbidden(
                "Only the recipient can save their experience or share a note."
            )
        with self.transaction():
            wish = self._wish(gift.wish_id, lock=True)
            gift, owner = self._authorized_experience(dto)
            if gift.status != "received":
                raise GiftConflict(
                    "Confirm the gift arrived before saving your experience."
                )
            if dto.action == "share_thanks" and not dto.thank_you:
                raise DomainValidationError(
                    {"thank_you": "Write a note before sharing it with your friend."}
                )
            if dto.action == "save_private" and not (
                {"fit", "private_note"} & dto.model_fields_set
            ):
                raise DomainValidationError({"fit": "Choose what to save privately."})
            if dto.action == "acknowledge_follow_up":
                if owner:
                    raise GiftForbidden(
                        "Only the giver can acknowledge the recipient's practical note."
                    )
                if not gift.follow_up_note:
                    raise GiftConflict("There is no practical note to acknowledge.")
                if gift.follow_up_acknowledged_at is None:
                    gift = self.repository.save_experience(dto, self.clock())
                    self.repository.notify(gift.owner_id, wish, "follow_up_seen")
                return self._experience_output(gift, False)
            if dto.action == "share_follow_up" and not dto.follow_up_note:
                raise DomainValidationError(
                    {
                        "follow_up_note": "Write the practical note you want your friend to see."
                    }
                )
            previous_follow_up = gift.follow_up_note
            previous_note = gift.thank_you
            gift = self.repository.save_experience(dto, self.clock())
            if (
                dto.action == "share_thanks"
                and gift.friend_id
                and self.profiles.exists(gift.friend_id)
                and dto.thank_you != previous_note
            ):
                self.repository.notify(gift.friend_id, wish, "thanks_shared")
            if (
                dto.action == "share_follow_up"
                and gift.friend_id
                and self.profiles.exists(gift.friend_id)
                and dto.follow_up_note != previous_follow_up
            ):
                self.repository.notify(gift.friend_id, wish, "follow_up_shared")
        return self._experience_output(gift, True)
