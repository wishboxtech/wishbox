from django.db import transaction

from src.apps.profile.models import Profile

@transaction.atomic
def create_profile(user_id, **kwargs):
    return Profile.objects.create(profile_id=user_id, **kwargs)