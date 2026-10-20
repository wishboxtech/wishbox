from django.contrib import admin

from src.apps.profile.models import Avatar
from unfold.admin import ModelAdmin


@admin.register(Avatar)
class AvatarAdmin(ModelAdmin):

    list_display = ("profile",)

    fields = (
        "profile",
        "settings",
        "created_at",
        "updated_at",
    )

    readonly_fields = ("created_at", "updated_at", "settings")
