import copy
from typing import Dict, Tuple


def apply_json_patches(data: Dict[Dict, Dict], updates: Dict[Tuple, str]):
    """
    Helper function to check the validation of structure in memory
    Example:

    ```python
    data = {
        "widgets": {
            "face": {"shape": "round", "fill_color": "blue"},
            "eyes": {"fill_color": "green"}
    }
    updates = {
        ("widgets", "face", "fill_color"): "red",
        ("widgets", "nose", "shape"): "round"
    }
    ````
    """

    new_data = copy.deepcopy(data)
    for path, value in updates.items():
        ref = new_data
        # Walk through the nested keys until the last one
        for key in path[:-1]:
            ref = ref.setdefault(key, {})
        # Set the final key to the new value
        ref[path[-1]] = value
    return new_data


def flatten_json(data, prefix=()):
    flat = {}

    for key, value in data.items():
        path = prefix + (key,)

        if isinstance(value, dict):
            flat.update(flatten_json(value, path))
        else:
            flat[path] = value

    return flat
