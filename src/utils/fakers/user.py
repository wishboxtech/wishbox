import factory
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "authentication.User"

    password = "foo"
    set_password = factory.PostGenerationMethodCall("set_password", "foo")
    phone_number = factory.Faker("numerify", text="09#########")
    email = None
