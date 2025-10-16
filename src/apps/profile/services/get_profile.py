from src.apps.profile.selectors import get_profile_by_id
from src.apps.profile.serializers import ReadProfileSerializer


def get_profile_by_user_id(id):
    """
    Return serialized profile data for a given user_id.
    Returns None if no profile exists.
    """
    profile = get_profile_by_id(profile_id=id)
    if profile is None:
        return None
    return ReadProfileSerializer(instance=profile, many=False).data