from copy import deepcopy
from uuid import UUID

from pydantic import ValidationError

from src.apps.profile.domain.avatar import AvatarSettings
from src.apps.profile.domain.errors import AvatarNotFound, InvalidAvatarSettings
from src.apps.profile.dto import (
    AvatarOutputDTO,
    AvatarSettingsOutputDTO,
    ProfileOutputDTO,
    RenderedWidgetDTO,
    UpdateAvatarInputDTO,
    UpsertProfileInputDTO,
    UpsertProfileOutputDTO,
)
from src.apps.profile.helpers import apply_json_patches, flatten_json
from src.apps.profile.interfaces import ProfileRepository, AuthenticationServiceProtocol
from src.apps.storage.interfaces import StorageServiceProtocol
from src.shared.domain.errors import DomainValidationError
from src.shared.dto import IdInputDTO
from src.shared.interfaces import TransactionBoundary


class ProfileService:
    def __init__(
        self,
        repository: ProfileRepository,
        authentication: AuthenticationServiceProtocol,
        storage: StorageServiceProtocol,
        transaction: TransactionBoundary,
    ):
        self.repository = repository
        self.authentication = authentication
        self.storage = storage
        self.transaction = transaction

    def exists(self, id: UUID) -> bool:
        return self.repository.exists(id)

    def _output(self, profile) -> ProfileOutputDTO:
        user = self.authentication.get_user(IdInputDTO(id=profile.profile_id))
        if user is None:
            raise DomainValidationError({"profile": "User does not exist."})
        return ProfileOutputDTO(
            profile_id=profile.profile_id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            birthdate=profile.birthdate,
            gender=profile.gender,
            bio=profile.bio,
            cat_avatar=profile.cat_avatar,
            photo=self.storage.get_media(profile.photo_id)
            if profile.photo_id
            else None,
            phone_number=user.phone_number,
            email=user.email,
            is_phone_number_verified=user.is_phone_number_verified,
            has_accepted_terms=user.has_accepted_terms,
        )

    def get_profile(self, dto: IdInputDTO) -> ProfileOutputDTO | None:
        profile = self.repository.get(dto.id)
        return self._output(profile) if profile else None

    def upsert_profile(self, dto: UpsertProfileInputDTO) -> UpsertProfileOutputDTO:
        with self.transaction():
            if self.authentication.get_user(IdInputDTO(id=dto.profile_id)) is None:
                raise DomainValidationError({"profile": "User does not exist."})
            if (
                dto.photo_id is not None
                and self.storage.get_media(dto.photo_id) is None
            ):
                raise DomainValidationError({"photo": "Media does not exist."})
            profile, created = self.repository.upsert(dto)
        return UpsertProfileOutputDTO(created=created, profile=self._output(profile))

    def get_avatar(self, dto: IdInputDTO) -> AvatarOutputDTO | None:
        settings = self.repository.get_avatar(dto.id)
        if settings is None:
            return None
        widgets = settings.widgets.model_dump()
        # Resolve by ID rather than list position: missing or repeated shapes must
        # never put another widget's image in the wrong slot.
        shape_ids = {}
        for name, widget in widgets.items():
            try:
                shape_ids[name] = UUID(widget["shape"])
            except ValueError:
                pass
        images = self.repository.widget_media_ids(tuple(shape_ids.values()))
        media = self.storage.get_media_batch(tuple(images.values()))
        rendered = {}
        for name, widget in widgets.items():
            media_id = images.get(shape_ids.get(name))
            rendered[name] = RenderedWidgetDTO(
                fill_color=widget["fill_color"],
                image=media.get(media_id),
            )
        return AvatarOutputDTO(
            wrapper_shape=settings.wrapper_shape,
            background=settings.background,
            gender=settings.gender,
            widgets=rendered,
        )

    def update_avatar(self, dto: UpdateAvatarInputDTO) -> AvatarSettingsOutputDTO:
        with self.transaction():
            settings = self.repository.get_avatar(dto.profile_id, lock=True)
            if settings is None:
                raise AvatarNotFound()
            try:
                patched = apply_json_patches(
                    settings.model_dump(), flatten_json(deepcopy(dto.changes))
                )
                new_settings = AvatarSettings.model_validate(patched)
            except (ValidationError, TypeError, AttributeError):
                raise InvalidAvatarSettings() from None
            self.repository.save_avatar(dto.profile_id, new_settings)
        return AvatarSettingsOutputDTO(settings=new_settings)
