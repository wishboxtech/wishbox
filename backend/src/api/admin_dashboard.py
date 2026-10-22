"""Presentation callback for Unfold's existing, protected admin index."""

from src.core.composition import dashboard_service


def dashboard_callback(request, context):
    # Product-wide reporting is reserved for superusers, not arbitrary staff.
    if not request.user.is_active or not request.user.is_superuser:
        return context
    metrics = dashboard_service().overview()
    peak = max((max(day.created, day.fulfilled) for day in metrics.daily), default=0)
    context["wishy_metrics"] = metrics
    context["wishy_trend"] = [
        {
            "day": day.day,
            "created": day.created,
            "fulfilled": day.fulfilled,
            "created_height": max(3, round(100 * day.created / peak))
            if day.created and peak
            else 0,
            "fulfilled_height": max(3, round(100 * day.fulfilled / peak))
            if day.fulfilled and peak
            else 0,
        }
        for day in metrics.daily
    ]
    return context
