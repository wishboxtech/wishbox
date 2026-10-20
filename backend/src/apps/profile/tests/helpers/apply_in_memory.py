import copy

from django.test import SimpleTestCase

from src.apps.profile.helpers import apply_json_patches, flatten_json


class JsonHelpersTestCase(SimpleTestCase):
    """
    Unit tests for:
    - apply_json_patches
    - flatten_json
    """

    def test_apply_json_patches_updates_existing_fields(self):
        data = {
            "widgets": {
                "face": {"shape": "round", "fill_color": "blue"},
                "eyes": {"fill_color": "green"},
            }
        }
        updates = {
            ("widgets", "face", "fill_color"): "red",
            ("widgets", "eyes", "fill_color"): "yellow",
        }

        result = apply_json_patches(data, updates)

        self.assertEqual(result["widgets"]["face"]["fill_color"], "red")
        self.assertEqual(result["widgets"]["eyes"]["fill_color"], "yellow")
        self.assertEqual(result["widgets"]["face"]["shape"], "round")  # untouched

    def test_apply_json_patches_creates_missing_paths(self):
        """
        Should create nested dictionaries if path does not exist.
        """
        data = {"widgets": {}}
        updates = {
            ("widgets", "nose", "shape"): "round",
            ("widgets", "nose", "fill_color"): "pink",
        }

        result = apply_json_patches(data, updates)

        self.assertEqual(result["widgets"]["nose"]["shape"], "round")
        self.assertEqual(result["widgets"]["nose"]["fill_color"], "pink")

    def test_apply_json_patches_does_not_modify_original(self):
        """
        Ensure deep copy works — original input must remain unchanged.
        """
        data = {"widgets": {"face": {"shape": "round"}}}
        updates = {("widgets", "face", "shape"): "square"}

        original = copy.deepcopy(data)
        result = apply_json_patches(data, updates)

        # original stays untouched
        self.assertEqual(data, original)
        # result is modified
        self.assertEqual(result["widgets"]["face"]["shape"], "square")

    def test_apply_json_patches_empty_updates(self):
        data = {"widgets": {"face": {"shape": "round"}}}
        updates = {}

        result = apply_json_patches(data, updates)
        self.assertEqual(result, data)

    def test_apply_json_patches_empty_data(self):
        data = {}
        updates = {("widgets", "face", "shape"): "round"}

        result = apply_json_patches(data, updates)
        self.assertEqual(result["widgets"]["face"]["shape"], "round")

    # -------------------------------------------------------------------------
    # flatten_json tests
    # -------------------------------------------------------------------------

    def test_flatten_json_basic(self):
        data = {
            "widgets": {
                "face": {"shape": "round", "fill_color": "blue"},
                "eyes": {"fill_color": "green"},
            }
        }

        flat = flatten_json(data)

        expected = {
            ("widgets", "face", "shape"): "round",
            ("widgets", "face", "fill_color"): "blue",
            ("widgets", "eyes", "fill_color"): "green",
        }

        self.assertEqual(flat, expected)

    def test_flatten_json_empty(self):
        self.assertEqual(flatten_json({}), {})

    def test_flatten_json_handles_nested_levels(self):
        data = {
            "a": {
                "b": {
                    "c": {"d": 5},
                },
            },
        }

        result = flatten_json(data)

        self.assertEqual(result, {("a", "b", "c", "d"): 5})

    # -------------------------------------------------------------------------
    # Round-trip correctness: flatten → apply must reconstruct original
    # -------------------------------------------------------------------------

    def test_round_trip_flatten_and_apply(self):
        """
        flatten_json() + apply_json_patches() should reconstruct the original dict.
        """
        data = {
            "widgets": {
                "face": {"shape": "round", "fill_color": "blue"},
                "eyes": {"fill_color": "green"},
                "nose": {"shape": "oval"},
            },
            "gender": "M",
        }

        flat = flatten_json(data)

        new = apply_json_patches({}, flat)
        self.assertEqual(new, data)
