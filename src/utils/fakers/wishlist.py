import factory
from faker import Faker

from src.utils.fakers.profile import ProfileFactory

fake = Faker()


class WishlistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "wishlist.Wishlist"

    profile = factory.SubFactory(ProfileFactory)
    name = factory.LazyAttribute(lambda _: fake.name())
    description = factory.LazyAttribute(lambda _: fake.text())
