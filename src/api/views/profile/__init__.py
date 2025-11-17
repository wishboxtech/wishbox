from src.api.views.profile.create_update_profile import CreateUpdateProfile
from src.api.views.profile.get_profile import GetProfileAPIView
from src.api.views.profile.get_avatar import GetAvatarAPIView
from src.api.views.profile.update_avatar import UpdateAvatarAPIView


class AvatarAPIView(GetAvatarAPIView, UpdateAvatarAPIView):
    pass


class ProfileAPIView(CreateUpdateProfile, GetProfileAPIView):
    pass
