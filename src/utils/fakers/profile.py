import factory
from src.utils.fakers.user import UserFactory

class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "profile.Profile"
    
    profile = factory.SubFactory(UserFactory)