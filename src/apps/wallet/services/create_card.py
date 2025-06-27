from django.db import transaction

from src.static.serializer_errors import SerializerErrors
from src.apps.wallet.serializers import CreateCardSerializer


@transaction.atomic
def create_card(data):
    errs = {}
    card = None
    done = False

    serializer = CreateCardSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        card = serializer.data
        done = True
    else:
        errors = serializer.errors
        error_types = []
        for error in errors.keys():
            error_type = SerializerErrors.CreateCard.errors.get(error)
            error_types.append(error_type)
        errs["errors"] = errors
        errs["error_type"] = error_types

    return card, errs, done
