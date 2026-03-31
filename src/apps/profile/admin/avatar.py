from django.contrib import admin

from src.apps.profile.models import Avatar

try:
    from unfold.admin import ModelAdmin
except ImportError:
    from django.contrib.admin import ModelAdmin


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
