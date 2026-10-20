from django.urls import reverse
from rest_framework.test import APITestCase

from src.utils.fakers import ProfileFactory, UserFactory


class CatProfileTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = ProfileFactory(profile_id=self.user.id)
        self.client.force_authenticate(self.user)

    def test_cat_recipe_roundtrips_and_omitted_recipe_is_preserved(self):
        recipe = {"version": 1, "eyes": 49, "face": 17, "fur": 15, "background": 11}
        response = self.client.put(
            reverse("profile"), {"cat_avatar": recipe}, format="json"
        )
        self.assertEqual(response.status_code, 202, response.data)
        self.assertEqual(response.data["data"]["cat_avatar"]["eyes"], 49)
        response = self.client.put(
            reverse("profile"), {"first_name": "Sara"}, format="json"
        )
        self.assertEqual(response.data["data"]["cat_avatar"]["face"], 17)
        self.assertEqual(
            self.client.get(reverse("profile")).data["data"]["cat_avatar"]["fur"], 15
        )
        response = self.client.put(
            reverse("profile"), {"cat_avatar": None}, format="json"
        )
        self.assertIsNone(response.data["data"]["cat_avatar"])

    def test_invalid_or_unknown_shapes_cannot_be_persisted(self):
        for recipe in (
            {"eyes": 50},
            {"nose": -1},
            {"mouth": 1.5},
            {"face": True},
            {"fur": 16},
            {"background": 12},
            {"version": 2},
            {"script": "unsafe"},
        ):
            response = self.client.put(
                reverse("profile"), {"cat_avatar": recipe}, format="json"
            )
            self.assertEqual(response.status_code, 400, (recipe, response.data))
        self.profile.refresh_from_db()
        self.assertIsNone(self.profile.cat_avatar)

    def test_recipe_cannot_override_the_profile_actor(self):
        other = ProfileFactory()
        response = self.client.put(
            reverse("profile"),
            {"profile_id": str(other.profile_id), "cat_avatar": {"face": 49}},
            format="json",
        )
        self.assertEqual(response.status_code, 202)
        other.refresh_from_db()
        self.assertIsNone(other.cat_avatar)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.cat_avatar["face"], 49)
