import json
import factory
from faker import Faker

from src.utils.fakers.profile import ProfileFactory

fake = Faker()


class AvatarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "profile.Avatar"

    profile = factory.SubFactory(ProfileFactory)
    settings = factory.LazyAttribute(
        lambda _: json.loads(
            fake.json(
                data_columns={
                    "gender": "passport_gender",
                    "widgets": {
                        "ear": {"shape": "slug", "fill_color": "color"},
                        "face": {"shape": "slug", "fill_color": "color"},
                        "tops": {"shape": "slug", "fill_color": "color"},
                        "eyes": {"shape": "slug", "fill_color": "color"},
                        "nose": {"shape": "slug", "fill_color": "color"},
                        "mouth": {"shape": "slug", "fill_color": "color"},
                        "beard": {"shape": "slug", "fill_color": "color"},
                        "clothes": {"shape": "slug", "fill_color": "color"},
                        "glasses": {"shape": "slug", "fill_color": "color"},
                        "earrings": {"shape": "slug", "fill_color": "color"},
                        "eyebrows": {"shape": "slug", "fill_color": "color"},
                    },
                },
                num_rows=1,
            ),
        )
    )
