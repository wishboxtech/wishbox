from src.apps.wishlist.serializers import WriteReservationRequestSerialzier
from src.static import SerializerErrors


def submit_request(data):
    """
    Create an Reserve Request based on the provided data
    """

    errs = {}
    created = False
    reservation_data = None

    error_dict = SerializerErrors.ReservationRequest.errors

    serializer = WriteReservationRequestSerialzier(
        data=data,
        partial=True,
    )

    if serializer.is_valid():
        instance = serializer.save()
        reservation_data = instance
        created = True
    else:
        error_types = []
        errors = serializer.errors
        for error in errors.keys():
            error_type = error_dict.get(error)
            error_types.append(error_type)
        errs["errors"] = errors
        errs["error_type"] = error_types
    return created, reservation_data, errs
