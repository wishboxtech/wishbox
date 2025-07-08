import factory


class MediaModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "storage.MediaModel"

    file = factory.django.FileField()
