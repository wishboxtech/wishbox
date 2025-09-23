from src.api.views.profile.get_profile import GetProfileAPIView
from src.api.views.profile.create_update_profile import CreateUpdateProfile


class ProfileAPIView(CreateUpdateProfile, GetProfileAPIView):
    pass
