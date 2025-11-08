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
                    "wrapper_shape": "slug",
                    "background": {
                        "color": "color",
                        "border_color": "color",
                    },
                    "widgets": {
                        "ear": {"shape": "uuid4", "fill_color": "color"},
                        "face": {"shape": "uuid4", "fill_color": "color"},
                        "tops": {"shape": "uuid4", "fill_color": "color"},
                        "eyes": {"shape": "uuid4", "fill_color": "color"},
                        "nose": {"shape": "uuid4", "fill_color": "color"},
                        "mouth": {"shape": "uuid4", "fill_color": "color"},
                        "beard": {"shape": "uuid4", "fill_color": "color"},
                        "clothes": {"shape": "uuid4", "fill_color": "color"},
                        "glasses": {"shape": "uuid4", "fill_color": "color"},
                        "earrings": {"shape": "uuid4", "fill_color": "color"},
                        "eyebrows": {"shape": "uuid4", "fill_color": "color"},
                    },
                },
                num_rows=1,
            ),
        )
    )
