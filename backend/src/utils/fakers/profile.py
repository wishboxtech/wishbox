import factory
from faker import Faker

from src.utils.fakers.user import UserFactory

fake = Faker()


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "profile.Profile"

    profile = factory.SubFactory(UserFactory)
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
