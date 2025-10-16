from src.api.views.profile.create_update_profile import CreateUpdateProfile
from src.api.views.profile.get_profile import GetProfileAPIView


class ProfileAPIView(CreateUpdateProfile, GetProfileAPIView):
    pass
