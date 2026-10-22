"""Aggregate wishes, not reservation attempts, for the admin overview."""

from datetime import timezone

from django.db.models import Case, CharField, Count, Q, Value, When
from django.db.models.functions import TruncDate

from src.apps.website.dto.dashboard import (
    DailyWishCountsDTO,
    GenderWishCountsDTO,
    WishMetricsDTO,
)
from src.apps.wishlist.models import ReservationRequest, Wish


class DjangoWishMetricsReader:
    def read(self, since, until):
        # Explicit received status is authoritative. Accepted/purchased are not delivery.
        fulfilled = Q(reservation_requests__status="received")
        wishes = Wish.objects.all()
        counts = wishes.aggregate(
            total=Count("pk", distinct=True),
            fulfilled=Count("pk", filter=fulfilled, distinct=True),
            reserved=Count(
                "pk", filter=Q(reservation_requests__status="reserved"), distinct=True
            ),
            purchased=Count(
                "pk", filter=Q(reservation_requests__status="purchased"), distinct=True
            ),
            recent=Count(
                "pk",
                filter=Q(created_at__gte=since, created_at__lte=until),
                distinct=True,
            ),
        )
        genders = (
            wishes.annotate(
                gender_group=Case(
                    When(wishlist__profile__gender="female", then=Value("female")),
                    When(wishlist__profile__gender="male", then=Value("male")),
                    default=Value("unknown"),
                    output_field=CharField(),
                )
            )
            .values("gender_group")
            .annotate(
                total=Count("pk", distinct=True),
                fulfilled=Count("pk", filter=fulfilled, distinct=True),
            )
            .order_by("gender_group")
        )
        daily = {}
        for row in (
            wishes.filter(created_at__gte=since, created_at__lte=until)
            .annotate(day=TruncDate("created_at", tzinfo=timezone.utc))
            .values("day")
            .annotate(count=Count("pk"))
            .order_by("day")
        ):
            daily[row["day"]] = {"day": row["day"], "created": row["count"]}
        for row in (
            ReservationRequest.objects.filter(
                status="received",
                wish__isnull=False,
                received_at__gte=since,
                received_at__lte=until,
            )
            .annotate(day=TruncDate("received_at", tzinfo=timezone.utc))
            .values("day")
            .annotate(count=Count("wish_id", distinct=True))
            .order_by("day")
        ):
            daily.setdefault(row["day"], {"day": row["day"]})["fulfilled"] = row[
                "count"
            ]
        return WishMetricsDTO(
            **counts,
            by_gender=tuple(
                GenderWishCountsDTO(
                    gender=row["gender_group"],
                    total=row["total"],
                    fulfilled=row["fulfilled"],
                )
                for row in genders
            ),
            daily=tuple(DailyWishCountsDTO(**row) for row in daily.values()),
        )
