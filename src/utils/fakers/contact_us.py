import factory
from faker import Faker
from src.apps.website.models import ContactUs

fake = Faker()

class ContactUsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactUs

    email = factory.LazyAttribute(lambda _: fake.email()) 
