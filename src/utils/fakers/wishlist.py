import factory
from src.utils.fakers.profile import ProfileFactory
from faker import Faker

fake = Faker()

class WishlistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "wishlist.Wishlist"
    
    profile = factory.SubFactory(ProfileFactory)
    name = factory.LazyAttribute(lambda _: fake.name())
    description = factory.LazyAttribute(lambda _: fake.text())