import random

import factory
from faker import Faker

from src.apps.profile.models import AvatarWidgets
from src.utils.fakers.media import MediaModelFactory

fake = Faker()


class AvatarWidgetsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "profile.AvatarWidgets"

    type = random.choice(AvatarWidgets.WidgetType.choices)
    image = factory.SubFactory(MediaModelFactory)
