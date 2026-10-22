"""Aggregate customer accounts without counting administration accounts."""

from django.db.models import Count, Q

from src.apps.authentication.models import User
from src.apps.website.dto.dashboard import UserMetricsDTO


class DjangoUserMetricsReader:
    def read(self, since, until):
        counts = User.objects.filter(
            type=User.UserType.NORMAL_USER, is_staff=False, is_superuser=False
        ).aggregate(
            total=Count("pk"),
            enabled=Count("pk", filter=Q(is_active=True)),
            active=Count(
                "pk",
                filter=Q(is_active=True, last_login__gte=since, last_login__lte=until),
            ),
            new=Count("pk", filter=Q(date_joined__gte=since, date_joined__lte=until)),
        )
        return UserMetricsDTO(**counts)
