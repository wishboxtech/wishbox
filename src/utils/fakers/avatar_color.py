import factory


class AvatarColorsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "profile.AvatarColors"

    color = factory.Faker("color")
