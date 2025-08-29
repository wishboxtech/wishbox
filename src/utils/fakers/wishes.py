import factory
from factory import fuzzy
from src.utils.fakers.wishlist import WishlistFactory
from faker import Faker

fake = Faker()


class WishFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "wishlist.Wish"

    wishlist = factory.SubFactory(WishlistFactory)
    name = factory.LazyAttribute(lambda _: fake.name())
    description = factory.LazyAttribute(lambda _: fake.text())
    price = fuzzy.FuzzyInteger(1000)
