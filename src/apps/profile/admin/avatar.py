from django.contrib import admin

from src.apps.profile.models import Avatar


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ("profile",)

    fields = (
        "profile",
        "settings",
        "created_at",
        "updated_at",
    )

    readonly_fields = ("created_at", "updated_at")
