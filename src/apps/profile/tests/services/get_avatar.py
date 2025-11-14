import uuid
from django.test import TestCase

from src.apps.profile.services import get_user_avatar
from src.apps.profile.models import AvatarWidgets
from src.utils.fakers import (
    AvatarFactory,
    AvatarWidgetsFactory,
    MediaModelFactory,
    ProfileFactory,
)
from src.apps.storage.services import serialize_media


class GetUserAvatarTestCase(TestCase):
    def setUp(self):
        """
        Create a valid profile, avatar widgets, and avatar with proper JSON settings
        matching AvatarSettings schema.
        """
        self.profile = ProfileFactory()

        self.widget_types = [
            "Ear",
            "Face",
            "Tops",
            "Eyes",
            "Nose",
            "Mouth",
            "Beard",
            "Clothes",
            "Glasses",
            "Earrings",
            "Eyebrows",
        ]

        self.widgets = {}
        self.widget_objs = []

        # Create real AvatarWidgets with MediaModel
        for wtype in self.widget_types:
            media = MediaModelFactory()
            widget = AvatarWidgetsFactory(type=wtype, image=media, is_active=True)
            self.widget_objs.append(widget)
            self.widgets[wtype.lower()] = {
                "shape": str(widget.id),
                "fill_color": "#ff00ff",
            }

        self.valid_settings = {
            "gender": "M",
            "wrapper_shape": "circle",
            "background": {"color": "#ffffff", "border_color": "#000000"},
            "widgets": self.widgets,
        }

        self.avatar = AvatarFactory(profile=self.profile, settings=self.valid_settings)

        print(self.avatar.settings)

    def test_get_user_avatar_success(self):
        """
        Should return a complete dict with images replacing shape IDs.
        """
        result = get_user_avatar(self.profile.profile_id)

        self.assertIsInstance(result, dict)
        self.assertIn("widgets", result)
        widgets = result["widgets"]

        # Check that all widgets now have 'image' instead of 'shape'
        for wname, widget_data in widgets.items():
            self.assertIn("image", widget_data)
            self.assertNotIn("shape", widget_data)
            self.assertEqual(widget_data["fill_color"], "#ff00ff")

            # Verify the image data comes from serialize_media
            image = widget_data["image"]
            media_obj = AvatarWidgets.objects.get(id=self.widgets[wname]["shape"]).image
            self.assertEqual(image, serialize_media(media_obj))

    def test_get_user_avatar_not_found(self):
        """
        Should return None if avatar does not exist for given profile ID.
        """
        random_profile_id = uuid.uuid4()
        result = get_user_avatar(random_profile_id)
        self.assertIsNone(result)
