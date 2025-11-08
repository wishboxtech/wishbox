import random

import factory
from faker import Faker

from src.utils.fakers.media import MediaModelFactory
from src.apps.profile.models import AvatarWidgets

fake = Faker()


class AvatarWidgetsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "profile.AvatarWidgets"

    type = random.choice(AvatarWidgets.WidgetType.choices)
    image = factory.SubFactory(MediaModelFactory)
