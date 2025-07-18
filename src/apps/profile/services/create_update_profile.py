from src.apps.profile.serializers import ReadProfileSerializer, WriteProfileSerializer
from src.apps.profile.selectors import get_profile_by_id
from src.static import SerializerErrors

def create_or_update_profile(user_id, data):
    """
    Create or update a user profile based on the provided data.
    """
    errs = {}
    created = False
    profile = None
    profile_data = None

    error_dict = SerializerErrors.CreateProfile.errors
    
    profile = get_profile_by_id(profile_id=user_id)
    serializer = WriteProfileSerializer(
        instance=profile,
        data=data,
        partial=True,
    )
    if serializer.is_valid():
        data = serializer.save()
        created = profile is None
        profile_data = ReadProfileSerializer(instance=data, many=False).data
    else:
        error_types = []
        errors = serializer.errors
        for error in errors.keys():
            error_type = error_dict.get(error)
            error_types.append(error_type)
        errs["errors"] = errors
        errs["error_type"] = error_types
    return created, profile_data, errs