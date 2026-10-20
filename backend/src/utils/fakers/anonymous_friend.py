import factory
from faker import Faker

from src.apps.wishlist.models import AnonymousFriend

fake = Faker()


class AnonymousFriendFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AnonymousFriend

    nickname = factory.LazyAttribute(lambda _: fake.name())
