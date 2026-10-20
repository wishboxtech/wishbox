from pydantic import ValidationError as DTOValidationError
from rest_framework import serializers

from src.shared.dto import DTO
from src.utils.exceptions import BadRequestException


class DTOResponseSerializer(serializers.BaseSerializer):
    """Render application data only. No model lookup or persistence."""

    def to_representation(self, instance):
        if isinstance(instance, DTO):
            return instance.model_dump(mode="json")
        raise TypeError("Responses must contain an output DTO.")


def input_dto(
    serializer_class, data, dto_class, *, error_codes=None, aliases=None, **context
):
    serializer = serializer_class(data=data)
    if not serializer.is_valid():
        raise BadRequestException(
            message=serializer.errors,
            error_type=[
                str((error_codes or {}).get(field, field))
                for field in serializer.errors
            ],
        )
    aliases = aliases or {}
    values = {
        aliases.get(key, key): value for key, value in serializer.validated_data.items()
    }
    values.update(context)
    try:
        return dto_class(**values)
    except DTOValidationError as error:
        reverse_aliases = {value: key for key, value in aliases.items()}
        errors = {
            reverse_aliases.get(str(item["loc"][0]), str(item["loc"][0])): item["msg"]
            for item in error.errors()
        }
        raise BadRequestException(
            message=errors,
            error_type=[str((error_codes or {}).get(field, field)) for field in errors],
        ) from error
