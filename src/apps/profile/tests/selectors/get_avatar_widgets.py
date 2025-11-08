import uuid
from django.test import TestCase

from src.apps.profile.models import AvatarWidgets
from src.apps.profile.selectors import (
    get_avatar_widgets,
    get_avatar_widget_images_by_id,
)
from src.utils.fakers import (
    AvatarWidgetsFactory,
    MediaModelFactory,
    AvatarColorsFactory,
)


class GetAvatarWidgetsSelectorsTestCase(TestCase):
    def setUp(self):
        self.media1 = MediaModelFactory()
        self.media2 = MediaModelFactory()
        self.media3 = MediaModelFactory()

        # Create three widgets with colors
        color1 = AvatarColorsFactory()
        color2 = AvatarColorsFactory()

        self.widget1 = AvatarWidgetsFactory(
            type="Face", image=self.media1, is_active=True
        )
        self.widget1.colors.add(color1)

        self.widget2 = AvatarWidgetsFactory(
            type="Eyes", image=self.media2, is_premium=True, is_active=True
        )
        self.widget2.colors.add(color2)

        self.widget3 = AvatarWidgetsFactory(
            type="Tops", image=self.media3, is_active=False
        )

    def test_get_avatar_widgets_returns_all_ordered_by_type(self):
        """
        Should return all AvatarWidgets ordered alphabetically by type.
        """
        widgets = get_avatar_widgets()

        # Order by type alphabetically: Ear < Eyes < Face < Tops ...
        db_widgets = list(AvatarWidgets.objects.all().order_by("type"))
        self.assertEqual(list(widgets), db_widgets)

        self.assertGreater(len(widgets), 0)
        self.assertIn(self.widget1, widgets)
        self.assertIn(self.widget2, widgets)

        # Check that only required fields are fetched
        self.assertTrue(hasattr(widgets[0], "type"))
        self.assertTrue(hasattr(widgets[0], "image"))
        # and colors should be prefetchable
        with self.assertNumQueries(0):
            list(widgets[0].colors.all())

    def test_get_avatar_widgets_empty(self):
        """
        Should return empty queryset if no AvatarWidgets exist.
        """
        AvatarWidgets.objects.all().delete()
        widgets = get_avatar_widgets()
        self.assertEqual(list(widgets), [])

    def test_get_avatar_widget_images_by_id_preserves_order(self):
        """
        Should return widgets in the exact same order as IDs provided.
        """
        ids = [self.widget3.id, self.widget1.id, self.widget2.id]
        result = list(get_avatar_widget_images_by_id(ids))

        self.assertEqual([w.id for w in result], ids)

        # Ensure only image field is loaded
        deferred_fields = result[0].get_deferred_fields()
        self.assertIn("type", deferred_fields)
        self.assertIn("is_active", deferred_fields)
        self.assertNotIn("image", deferred_fields)

    def test_get_avatar_widget_images_by_id_with_missing_id(self):
        """
        Should return only existing widgets and ignore missing IDs, preserving order of valid ones.
        """
        fake_id = uuid.uuid4()
        ids = [self.widget1.id, fake_id, self.widget3.id]

        result = list(get_avatar_widget_images_by_id(ids))
        result_ids = [w.id for w in result]

        # Fake ID should not appear
        self.assertIn(self.widget1.id, result_ids)
        self.assertIn(self.widget3.id, result_ids)
        self.assertNotIn(fake_id, result_ids)

        # Should still maintain the relative order of found IDs
        self.assertEqual(result_ids, [self.widget1.id, self.widget3.id])

    def test_get_avatar_widget_images_by_id_empty_list(self):
        """
        Should return empty queryset if no IDs provided.
        """
        result = list(get_avatar_widget_images_by_id([]))
        self.assertEqual(result, [])
