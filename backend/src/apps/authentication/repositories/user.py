from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.timezone import now

from src.apps.authentication.domain import User as UserEntity
from src.apps.authentication.models.user import User
from src.shared.domain.errors import DomainValidationError


def user_entity(item):
    return UserEntity(
        id=item.id,
        phone_number=item.phone_number,
        email=item.email,
        is_active=item.is_active,
        is_phone_number_verified=item.is_phone_number_verified,
        has_accepted_terms=item.has_accepted_terms,
    )


class DjangoUserRepository:
    def record_login(self, id):
        User.objects.filter(pk=id).update(last_login=now())

    def get(self, id):
        item = User.objects.filter(id=id).first()
        return user_entity(item) if item else None

    def find(self, identifier):
        item = User.objects.filter(
            Q(phone_number=identifier) | Q(email=identifier)
        ).first()
        return user_entity(item) if item else None

    def create(self, dto):
        try:
            item = User.objects.create_user(**dto.model_dump())
        except ValidationError as error:
            errors = getattr(error, "message_dict", {"user": error.messages})
            raise DomainValidationError(
                {key: str(value) for key, value in errors.items()}
            ) from error
        except ValueError as error:
            raise DomainValidationError({"user": str(error)}) from error
        return user_entity(item)
