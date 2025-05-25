from json import load
from numpy import uint16, float32
from typing import Dict, List, Tuple, Union

def get_ingredient_adjacency_lists(
    file_path: str
) -> Dict[str, List[Tuple[Union[uint16, str], uint16]]]:
    """
    get_ingredient_adjacency_lists (function)

    Reads a JSON file containing ingredient data and creates an adjacency list
    representation of the ingredients and their effects.
    
    Returns the adjacency list as a dictionary. The keys are the ingredient ids
    and the values are lists of tuples. Each tuple contains the effect ids that
    the ingredient can produce, and the corresponding effects that get
    transformed. The first tuple in the list of tuples contains the name of the
    ingredient and the effect given by the ingredient. The rest of the tuples
    contain the effect ids that get transformed by the ingredient. This is the
    direct consequence of the compacting data. Make sure when you use this that
    you are always adding the first element in the list before transforming a
    given mixture.

    For more information, see the class docstring for class Mix in mix.py.

    Parameters
    ----------
    file_path : str
        Path to the JSON file.

    Raises
    ------
    ValueError
        If the JSON file contains invalid data types for ingredient_id, name,
        effect_given, or effect_replaces_on_mix.

    Returns
    -------
    Dict[str, List[Tuple[uint16 | str, uint16]]]
        Adjacency list.
    """
    # Read the JSON with the ingredients
    ingredients_json: Dict = {}
    with open(file_path, 'r') as file:
        ingredients_json = load(file)

    # Make the adjacency list as a dictionary
    adj_lists: Dict[str, List[Tuple[Union[uint16, str], uint16]]] = {}

    # Iterate through the ingredients
    for ingredient in ingredients_json.keys():
        # Ensure ingredient is a string before using it as a key
        if not isinstance(ingredient, str):
            raise ValueError(
                f"Invalid type for ingredient: {type(ingredient)} in ingredients_json"
            )

        # Get the effect_given value
        effect_given_value = ingredients_json[ingredient]['effect_given']

        # Ensure effect_given_value is an int before converting to uint16
        if not isinstance(effect_given_value, int):
            raise ValueError(
                f"Invalid type for effect_given: {type(effect_given_value)} in ingredient {ingredient}"
            )

        # Ensure the name is a string before adding to the adjacency list
        if not isinstance(ingredients_json[ingredient]['name'], str):
            raise ValueError(
                f"Invalid type for name: {type(ingredients_json[ingredient]['name'])} in ingredient {ingredient}"
            )

        # Add initial tuple to the adjacency list
        adj_lists[ingredient] = [
            (ingredients_json[ingredient]['name'], uint16(effect_given_value))
        ]

        # Get the effect_replaces_on_mix dictionary
        effect_replaces_on_mix = ingredients_json[ingredient]['replaces_on_mix']

        # Ensure effect_replaces_on_mix is a dictionary before iterating
        if not isinstance(effect_replaces_on_mix, dict):
            raise ValueError(
                f"Invalid type for replaces_on_mix: {type(effect_replaces_on_mix)} in ingredient {ingredient}"
            )

        for effect in effect_replaces_on_mix.keys():
            # Ensure effect is a string before converting to uint16
            if not isinstance(effect, str):
                raise ValueError(
                    f"Invalid type for effect: {type(effect)} in ingredient {ingredient}"
                )

            # Ensure effect_replaces_on_mix[effect] is an int before converting to uint16
            if not isinstance(effect_replaces_on_mix[effect], int):
                raise ValueError(
                    f"Invalid type for effect_replaces_on_mix[effect]: {type(effect_replaces_on_mix[effect])} in ingredient {ingredient}"
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
    get_effect_details (function)

    Reads a JSON file containing effect data and creates a dictionary of effect
    details. Each effect is represented by a dictionary containing its name and
    value. The values are exact copies of the values in the JSON file. They are
    not mutated in any way.

    Parameters
    ----------
    file_path : str
        Path to the JSON file.

    Raises
    ------
    ValueError
        If the JSON file contains invalid data types for effect_id, name, or
        value.
        
    Returns
    -------
    Dict[str, Dict[str, str | float32]]
        Dictionary of effect details.
    """
    # Read the JSON with the effects
    effects_json: Dict = {}
    with open(file_path, 'r') as file:
        effects_json = load(file)

    # Make the effects list as a dictionary
    effects_details: Dict[str, Dict[str, Union[str, float32]]] = {}

    # Iterate through the effects
    for effect_id in effects_json.keys():
        # Ensure effect_id is a string before using it as a key
        if not isinstance(effect_id, str):
            raise ValueError(
                f"Invalid type for effect_id: {type(effect_id)} in effects_json"
            )

        # Ensure effects_json[effect_id] is a dictionary before using it
        if not isinstance(effects_json[effect_id], dict):
            raise ValueError(
                f"Invalid type for effects_json[effect_id]: {type(effects_json[effect_id])} in effects_json"
            )

        # Ensure effects_json[effect_id]['name'] is a string before using it
        if not isinstance(effects_json[effect_id]['name'], str):
            raise ValueError(
                f"Invalid type for effects_json[effect_id]['name']: {type(effects_json[effect_id]['name'])} in effects_json"
            )

        # Ensure effects_json[effect_id]['value'] is a float before using it
        if not isinstance(effects_json[effect_id]['value'], float):
            raise ValueError(
                f"Invalid type for effects_json[effect_id]['value']: {type(effects_json[effect_id]['value'])} in effects_json"
            )

        # Add entry to the effects list
        effects_details[effect_id] = {
            'name': effects_json[effect_id]['name'],
            'value': float32(effects_json[effect_id]['value'])
        }

    return effects_details