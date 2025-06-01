from json import load
from typing import Dict, List, Tuple, Union

from numpy import float32, uint16

class InvalidFileExtentionError(Exception):
    """
    Raised when the file extension is not supported.

    Attributes
    ----------
    message : str
        Error message indicating the invalid file extension.
    """
    def __init__(self, message: str = "Invalid file extension.") -> None:
        self.message = message
        super().__init__(self.message)

class MissingKeyError(Exception):
    """
    Raised when a required key is missing in the JSON data.

    Attributes
    ----------
    message : str
        Error message indicating the missing key.
    """
    def __init__(self, message: str = "Missing required key in JSON data.") -> None:
        self.message = message
        super().__init__(self.message)

def get_ingredient_adjacency_lists(
    file_path: str
) -> Dict[str, List[Tuple[Union[uint16, str], uint16]]]:
    """
    Reads a JSON file containing ingredient data and creates an adjacency list
    representation of the ingredients and their effects.

    Returns the adjacency list as a dictionary. The keys are the ingredient IDs,
    and the values are lists of tuples. Each tuple contains the effect IDs that
    the ingredient can produce, and the corresponding effects that get
    transformed. The first tuple in the list contains the name of the ingredient
    and the effect given by the ingredient. The rest of the tuples contain the
    effect IDs that get transformed by the ingredient.

    For more information, see the class docstring for the class Mix in mix.py.

    Parameters
    ----------
    file_path : str
        Path to the JSON file.

    Raises
    ------
    FileNotFoundError
        If the JSON file does not exist at the specified path.
    InvalidFileExtentionError
        If the file does not have a .json extension.
    MissingKeyError
        If the JSON file does not contain the required keys for each ingredient.
    ValueError
        If the JSON file contains invalid data types for ingredient_id, name,
        effect_given, or effect_replaces_on_mix.

    Returns
    -------
    Dict[str, List[Tuple[uint16 | str, uint16]]]
        Adjacency list.
    """
    # Ensure the file has a .json extension
    if not file_path.endswith('.json'):
        raise InvalidFileExtentionError(
            "The file must have a .json extension."
        )

    # Read the JSON with the ingredients
    ingredients_json: Dict = {}
    try:
        with open(file_path, 'r') as file:
            ingredients_json = load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e

    # Create the adjacency list as a dictionary
    adj_lists: Dict[str, List[Tuple[Union[uint16, str], uint16]]] = {}

    # Iterate through the ingredients
    for ingredient in ingredients_json.keys():
        # Ensure ingredients_json[ingredient] is a dictionary
        if not isinstance(ingredients_json[ingredient], dict):
            raise ValueError(
                f"Invalid type for ingredients_json[ingredient]: "
                f"{type(ingredients_json[ingredient])} in ingredient '{ingredient}'"
            )

        # Ensure required keys are present
        required_keys = {'name', 'effect_given', 'replaces_on_mix'}
        if not required_keys.issubset(ingredients_json[ingredient].keys()):
            missing = required_keys - set(ingredients_json[ingredient].keys())
            raise MissingKeyError(
                f"Missing required keys in ingredient {ingredient}: {missing}"
            )

        # Ensure 'name' is a string
        if not isinstance(ingredients_json[ingredient]['name'], str):
            raise ValueError(
                f"Invalid type for name: "
                f"{type(ingredients_json[ingredient]['name'])} in ingredient '{ingredient}'"
            )

        # Ensure 'effect_given' is an int
        if not isinstance(ingredients_json[ingredient]['effect_given'], int):
            raise ValueError(
                f"Invalid type for effect_given: "
                f"{type(ingredients_json[ingredient]['effect_given'])} in ingredient '{ingredient}'"
            )

        # Ensure 'replaces_on_mix' is a dictionary
        if not isinstance(ingredients_json[ingredient]['replaces_on_mix'], dict):
            raise ValueError(
                f"Invalid type for replaces_on_mix: "
                f"{type(ingredients_json[ingredient]['replaces_on_mix'])} in ingredient '{ingredient}'"
            )

        # Get the effect_given value
        effect_given_value = ingredients_json[ingredient]['effect_given']

        # Add initial tuple to the adjacency list
        adj_lists[ingredient] = [
            (ingredients_json[ingredient]['name'], uint16(effect_given_value))
        ]

        # Get the replaces_on_mix dictionary
        effect_replaces_on_mix = ingredients_json[ingredient]['replaces_on_mix']

        # Add the effects to the adjacency list
        for effect in effect_replaces_on_mix.keys():
            # Ensure effect translation value is an int
            if not isinstance(effect_replaces_on_mix[effect], int):
                raise ValueError(
                    f"Invalid type for effect translation value: "
                    f"{type(effect_replaces_on_mix[effect])} in ingredient '{ingredient}'"
                )

            # Add the effect to the adjacency list
            adj_lists[ingredient].append(
                (uint16(int(effect)), uint16(effect_replaces_on_mix[effect]))
            )

    return adj_lists

def get_effect_details(
    file_path: str
) -> Dict[str, Dict[str, Union[str, float32]]]:
    """
    Reads a JSON file containing effect data and creates a dictionary of effect
    details. Each effect is represented by a dictionary containing its name and
    value. The values are exact copies of the values in the JSON file.

    Parameters
    ----------
    file_path : str
        Path to the JSON file.

    Raises
    ------
    FileNotFoundError
        If the JSON file does not exist at the specified path.
    InvalidFileExtentionError
        If the file does not have a .json extension.
    ValueError
        If the JSON file contains invalid data types for effect_id, name, or
        value.

    Returns
    -------
    Dict[str, Dict[str, str | float32]]
        Dictionary of effect details.
    """
    # Ensure the file has a .json extension
    if not file_path.endswith('.json'):
        raise InvalidFileExtentionError(
            "The file must have a .json extension."
        )

    # Read the JSON with the effects
    effects_json: Dict = {}
    try:
        with open(file_path, 'r') as file:
            effects_json = load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e

    # Create the effects list as a dictionary
    effects_details: Dict[str, Dict[str, Union[str, float32]]] = {}

    # Iterate through the effects
    for effect_id in effects_json.keys():
        # Ensure effect_id is a string
        if not isinstance(effect_id, str):
            raise ValueError(
                f"Invalid type for effect_id: {type(effect_id)} in effects_json"
            )

        # Ensure effects_json[effect_id] is a dictionary
        if not isinstance(effects_json[effect_id], dict):
            raise ValueError(
                f"Invalid type for effects_json[effect_id]: "
                f"{type(effects_json[effect_id])} in effects_json"
            )

        # Ensure effects_json[effect_id]['name'] is a string
        if not isinstance(effects_json[effect_id]['name'], str):
            raise ValueError(
                f"Invalid type for effects_json[effect_id]['name']: "
                f"{type(effects_json[effect_id]['name'])} in effects_json"
            )

        # Ensure effects_json[effect_id]['value'] is a float
        if not isinstance(effects_json[effect_id]['value'], float):
            raise ValueError(
                f"Invalid type for effects_json[effect_id]['value']: "
                f"{type(effects_json[effect_id]['value'])} in effects_json"
            )

        # Add entry to the effects list
        effects_details[effect_id] = {
            'name': effects_json[effect_id]['name'],
            'value': float32(effects_json[effect_id]['value'])
        }

    return effects_details