from src.apps.profile.domain import Profile as ProfileEntity
from src.apps.profile.domain.avatar import AvatarSettings
from src.apps.profile.domain.errors import AvatarNotFound
from src.apps.profile.models import Avatar, AvatarWidgets, Profile


def profile_entity(item):
    return ProfileEntity(
        profile_id=item.profile_id,
        first_name=item.first_name,
        last_name=item.last_name,
        birthdate=item.birthdate,
        gender=item.gender,
        bio=item.bio,
        photo_id=item.photo_id,
    )


class DjangoProfileRepository:
    def exists(self, id):
        return Profile.objects.filter(profile_id=id).exists()

    def get(self, id):
        item = Profile.objects.filter(profile_id=id).first()
        return profile_entity(item) if item else None

    def upsert(self, dto):
        defaults = dto.model_dump(exclude_unset=True, exclude={"profile_id"})
        item, created = Profile.objects.update_or_create(
            profile_id=dto.profile_id, defaults=defaults
        )
        return profile_entity(item), created

    def get_avatar(self, id, *, lock=False):
        query = Avatar.objects.all()
        if lock:
            query = query.select_for_update()
        item = query.filter(profile_id=id).first()
        return (
            AvatarSettings.model_validate(item.settings)
            if item and item.settings
            else None
        )

    def save_avatar(self, id, settings):
        if (
            Avatar.objects.filter(profile_id=id).update(settings=settings.model_dump())
            == 0
        ):
            raise AvatarNotFound()

    def widget_media_ids(self, ids):
        return dict(
            AvatarWidgets.objects.filter(id__in=ids).values_list("id", "image_id")
        )
