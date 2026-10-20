from datetime import date, datetime, time, timedelta, timezone
from src.shared.domain.errors import DomainValidationError
from src.apps.wishlist.domain.gifting import GiftConflict


def require_purchase_date(purchase_by: date | None, now: datetime):
    if purchase_by is None or not now.date() <= purchase_by <= now.date() + timedelta(
        days=30
    ):
        raise DomainValidationError(
            {"purchase_by": "Choose a day from today through the next 30 days."}
        )


def reservation_times(purchase_by: date, now: datetime):
    # UTC end-of-date plus a buffer covers the chosen calendar day in all time zones.
    expires = datetime.combine(
        purchase_by + timedelta(days=2), time.min, tzinfo=timezone.utc
    )
    reminder = max(
        now + timedelta(hours=6),
        datetime.combine(purchase_by, time.min, tzinfo=timezone.utc),
    )
    return expires, reminder


def require_extension(gift, purchase_by: date | None, now: datetime):
    if gift.status != "reserved" or gift.extension_count >= 1:
        raise GiftConflict(
            "A reservation can be rescheduled once, before it expires or is bought."
        )
    require_purchase_date(purchase_by, now)
    if (
        gift.purchase_by is None
        or not gift.purchase_by < purchase_by <= gift.purchase_by + timedelta(days=7)
    ):
        raise DomainValidationError(
            {
                "purchase_by": "Choose a later day, up to 7 days after your original plan."
            }
        )
