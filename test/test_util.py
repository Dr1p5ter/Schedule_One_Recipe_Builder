from numpy import float32, issubdtype, uint16
from os import path
from pytest import raises
from sys import path as syspath

# Add parent directory to sys.path so we can import util
syspath.insert(0, path.abspath(path.join(path.dirname(__file__), '..')))

import util

# Paths to the test data files
TEST_FILE_NOT_FOUND_POINTER: str = path.join(
    path.dirname(__file__), "assets/test_not_found.json"
)
TEST_INVALID_FILE_EXTENSION: str = path.join(
    path.dirname(__file__), "assets/test_bad_extension.txt"
)

# Paths to the test ingredients data files
TEST_INGREDIENTS_INVALID_VALUE_TYPE_1_JSON: str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_invalid_value_type_1.json"
)
TEST_INGREDIENTS_INVALID_VALUE_TYPE_2_JSON: str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_invalid_value_type_2.json"
)
TEST_INGREDIENTS_INVALID_VALUE_TYPE_3_JSON: str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_invalid_value_type_3.json"
)
TEST_INGREDIENTS_INVALID_VALUE_TYPE_4_JSON: str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_invalid_value_type_4.json"
)
TEST_INGREDIENTS_INVALID_VALUE_TYPE_5_JSON: str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_invalid_value_type_5.json"
)
TEST_INGREDIENTS_JSON: str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients.json"
)
TEST_INGREDIENTS_MISSING_KEY: str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_missing_keys.json"
)
TEST_INGREDIENTS_SMALL_JSON: str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_small.json"
)

# Paths to the test effects data files
TEST_EFFECTS_INVALID_VALUE_TYPE_1_JSON: str = path.join(
    path.dirname(__file__), "assets/test_sample_effects_invalid_value_type_1.json"
)
TEST_EFFECTS_INVALID_VALUE_TYPE_2_JSON: str = path.join(
    path.dirname(__file__), "assets/test_sample_effects_invalid_value_type_2.json"
)
TEST_EFFECTS_INVALID_VALUE_TYPE_3_JSON: str = path.join(
    path.dirname(__file__), "assets/test_sample_effects_invalid_value_type_3.json"
)
TEST_EFFECTS_JSON: str = path.join(
    path.dirname(__file__), "assets/test_sample_effects.json"
)
TEST_EFFECTS_MISSING_KEY: str = path.join(
    path.dirname(__file__), "assets/test_sample_effects_missing_keys.json"
)

"""
Testing the function get_ingredient_adjacency_lists
"""

def test_get_ingredient_adjacency_lists_basic():
    """Test function with a basic JSON input."""
    adj_lists = util.get_ingredient_adjacency_lists(TEST_INGREDIENTS_JSON)

    # Check the adjacency list for the first ingredient
    assert adj_lists['0'] == [
        ('test_ingredient_0', uint16(0)),
        (uint16(1), uint16(2)),
        (uint16(3), uint16(4))
    ]

    # Check the adjacency list for a middle ingredient
    assert adj_lists['5'] == [
        ('test_ingredient_5', uint16(5)),
        (uint16(6), uint16(7)),
        (uint16(1), uint16(8))
    ]

    # Check the adjacency list for the last ingredient
    assert adj_lists['8'] == [
        ('test_ingredient_8', uint16(8)),
        (uint16(4), uint16(2)),
        (uint16(5), uint16(6))
    ]

    pass

def test_get_ingredient_adjacency_lists_small():
    """
    Test function with a JSON input where the ingredient has no replaces_on_mix.
    """
    adj_lists = util.get_ingredient_adjacency_lists(TEST_INGREDIENTS_SMALL_JSON)

    # Check the adjacency list for the ingredient
    assert adj_lists['0'] == [
        ('test_ingredient_0', uint16(0))
    ]

    pass

def test_get_ingredient_adjacency_lists_typing():
    """
    Ensure that the function returns the correct types.
    This is a catch-all from value_error tests.
    """
    adj_lists = util.get_ingredient_adjacency_lists(TEST_INGREDIENTS_JSON)

    # Check the type of the adjacency list
    assert isinstance(adj_lists, dict)

    # Check the type of the first ingredient's adjacency list
    assert isinstance(adj_lists['0'], list)

    # Check the type of the first ingredient's adjacency list elements
    assert isinstance(adj_lists['0'][0], tuple)

    # Check the type of the first element of the first ingredient's adjacency list
    assert isinstance(adj_lists['0'][0][0], str)  # name should be a string
    assert issubdtype(adj_lists['0'][0][1], uint16)  # effect_given should be an int
    assert issubdtype(adj_lists['0'][1][0], uint16)  # effect key should be an int
    assert issubdtype(adj_lists['0'][1][1], uint16)  # effect translation value should be an int

    pass

def test_get_ingredient_adjacency_lists_value_error_1():
    """
    Ensure ValueError is raised when the ingredient is not a dictionary.
    This test is for the case where the ingredient is an integer.
    Effected ingredient with id 1 in test JSON file.
    """
    with raises(ValueError) as e:
        util.get_ingredient_adjacency_lists(TEST_INGREDIENTS_INVALID_VALUE_TYPE_1_JSON)

    # Check the message raised exception
    assert str(e.value) == (
        "Invalid type for ingredients_json[ingredient]: <class 'int'> in ingredient '1'"
    )

    pass

def test_get_ingredient_adjacency_lists_value_error_2():
    """
    Ensure ValueError is raised when the ingredient name is not a string.
    This test is for the case where the ingredient name is an integer.
    Effected ingredient with id 2 in test JSON file.
    """
    with raises(ValueError) as e:
        util.get_ingredient_adjacency_lists(TEST_INGREDIENTS_INVALID_VALUE_TYPE_2_JSON)

    # Check the message raised exception
    assert str(e.value) == (
        "Invalid type for name: <class 'int'> in ingredient '2'"
    )

    pass

def test_get_ingredient_adjacency_lists_value_error_3():
    """
    Ensure ValueError is raised when the effect_given is not an int.
    This test is for the case where the effect_given is a string.
    Effected ingredient with id 3 in test JSON file.
    """
    with raises(ValueError) as e:
        util.get_ingredient_adjacency_lists(TEST_INGREDIENTS_INVALID_VALUE_TYPE_3_JSON)

    # Check the message raised exception
    assert str(e.value) == (
        "Invalid type for effect_given: <class 'str'> in ingredient '3'"
    )

    pass

def test_get_ingredient_adjacency_lists_value_error_4():
    """
    Ensure ValueError is raised when replaces_on_mix is not a dictionary.
    This test is for the case where replaces_on_mix is a list.
    Effected ingredient with id 4 in test JSON file.
    """
    with raises(ValueError) as e:
        util.get_ingredient_adjacency_lists(TEST_INGREDIENTS_INVALID_VALUE_TYPE_4_JSON)

    # Check the message raised exception
    assert str(e.value) == (
        "Invalid type for replaces_on_mix: <class 'list'> in ingredient '4'"
    )

    pass

def test_get_ingredient_adjacency_lists_value_error_5():
    """
    Ensure ValueError is raised when the effect translation value is not an int.
    This test is for the case where the effect translation value is a string.
    Effected ingredient with id 5 in test JSON file.
    """
    with raises(ValueError) as e:
        util.get_ingredient_adjacency_lists(TEST_INGREDIENTS_INVALID_VALUE_TYPE_5_JSON)

    # Check the message raised exception
    assert str(e.value) == (
        "Invalid type for effect translation value: <class 'str'> in ingredient '5'"
    )

    pass

def test_get_ingredient_adjacency_lists_missing_key_error():
    """
    Ensure that a MissingKeyError is raised when a required key is missing in
    the JSON file.
    """
    with raises(util.MissingKeyError) as e:
        util.get_ingredient_adjacency_lists(TEST_INGREDIENTS_MISSING_KEY)

    # Check the message raised exception
    assert (
        str(e.value) == "Missing required keys in ingredient 3: {'effect_given', 'name'}" or
        str(e.value) == "Missing required keys in ingredient 3: {'name', 'effect_given'}"
    )

    pass

def test_get_ingredient_adjacency_lists_file_not_found_error():
    """
    Ensure that a FileNotFoundError is raised when the file does not exist.
    """
    with raises(FileNotFoundError) as e:
        util.get_ingredient_adjacency_lists(TEST_FILE_NOT_FOUND_POINTER)

    # Check the message raised exception
    assert str(e.value) == (
        f"File not found: {TEST_FILE_NOT_FOUND_POINTER}"
    )

    pass

def test_get_ingredient_adjacency_lists_file_incorrect_extension():
    """
    Ensure that an InvalidFileExtentionError is raised when the file does not
    have a .json extension.
    """
    with raises(util.InvalidFileExtentionError) as e:
        util.get_ingredient_adjacency_lists(TEST_INVALID_FILE_EXTENSION)

    # Check the message raised exception
    assert str(e.value) == "The file must have a .json extension."

    pass

"""
Testing the function get_effect_details
"""

def test_get_effect_details_basic():
    """Test function with a basic JSON input."""
    effect_details = util.get_effect_details(TEST_EFFECTS_JSON)

    # Check the effect details for the first effect
    assert effect_details['0'] == {
        'name': 'effect_0',
        'value': float32(0.12),
    }

    # Check the effect details for a middle effect
    assert effect_details['5'] == {
        'name': 'effect_5',
        'value': float32(0.41),
    }

    # Check the effect details for the last effect
    assert effect_details['8'] == {
        'name': 'effect_8',
        'value': float32(0.29),
    }

    pass

def test_get_effect_details_typing():
    """
    Ensure that the function returns the correct types.
    This is a catch-all from value_error tests.
    """
    effect_details = util.get_effect_details(TEST_EFFECTS_JSON)

    # Check the type of the effect details
    assert isinstance(effect_details, dict)

    # Check the type of the first effect's details
    assert isinstance(effect_details['0'], dict)

    # Check the type of the first effect's name
    assert isinstance(effect_details['0']['name'], str)  # name should be a string

    # Check the type of the first effect's value
    assert issubdtype(effect_details['0']['value'], float32)  # value should be a float

    pass

def test_get_effect_details_value_error_1():
    """
    Ensure ValueError is raised when the effect is not a dictionary.
    This test is for the case where the effect is an integer.
    Effected effect with id 1 in test JSON file.
    """
    with raises(ValueError) as e:
        util.get_effect_details(TEST_EFFECTS_INVALID_VALUE_TYPE_1_JSON)

    # Check the message raised exception
    assert str(e.value) == (
        "Invalid type for effects_json[effect_id]: <class 'int'> in effect '1'"
    )

    pass

def test_get_effect_details_value_error_2():
    """
    Ensure ValueError is raised when the effect name is not a string.
    This test is for the case where the effect name is an integer.
    Effected effect with id 2 in test JSON file.
    """
    with raises(ValueError) as e:
        util.get_effect_details(TEST_EFFECTS_INVALID_VALUE_TYPE_2_JSON)

    # Check the message raised exception
    assert str(e.value) == (
        "Invalid type for effect name: <class 'int'> in effect '2'"
    )

    pass

def test_get_effect_details_value_error_3():
    """
    Ensure ValueError is raised when the effect value is not a float.
    This test is for the case where the effect value is a string.
    Effected effect with id 3 in test JSON file.
    """
    with raises(ValueError) as e:
        util.get_effect_details(TEST_EFFECTS_INVALID_VALUE_TYPE_3_JSON)

    # Check the message raised exception
    assert str(e.value) == (
        "Invalid type for effect value: <class 'str'> in effect '3'"
    )

    pass

def test_get_effect_details_missing_key_error():
    """
    Ensure that a MissingKeyError is raised when a required key is missing in
    the JSON file.
    """
    with raises(util.MissingKeyError) as e:
        util.get_effect_details(TEST_EFFECTS_MISSING_KEY)

    # Check the message raised exception
    assert str(e.value) == "Missing required keys in effect 1: {'value'}"

    pass

def test_get_effect_details_file_not_found_error():
    """
    Ensure that a FileNotFoundError is raised when the file does not exist.
    """
    with raises(FileNotFoundError) as e:
        util.get_effect_details(TEST_FILE_NOT_FOUND_POINTER)

    # Check the message raised exception
    assert str(e.value) == (
        f"File not found: {TEST_FILE_NOT_FOUND_POINTER}"
    )

    pass

def test_get_effect_details_file_incorrect_extension():
    """
    Ensure that an InvalidFileExtentionError is raised when the file does not
    have a .json extension.
    """
    with raises(util.InvalidFileExtentionError) as e:
        util.get_effect_details(TEST_INVALID_FILE_EXTENSION)

    # Check the message raised exception
    assert str(e.value) == "The file must have a .json extension."

    pass