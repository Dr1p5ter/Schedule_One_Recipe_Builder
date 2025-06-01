# make sure scope of test includes parent directory
from sys import path as syspath
from os import path
syspath.insert(0, path.abspath(path.join(path.dirname(__file__), '..')))

# Paths to the test ingredients data files
TEST_INGREDIENTS_JSON : str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients.json"
)
TEST_INGREDIENTS_SMALL_JSON : str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_small.json"
)
TEST_INGREDIENTS_INVALID_FILE_EXTENSION : str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_invalid_file_extension.txt"
)
TEST_INGREDIENTS_FILE_NOT_FOUND_POINTER : str = path.join(
    path.dirname(__file__), "assets/test_test_test_test.json"
)
TEST_INGREDIENTS_MISSING_KEY : str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_missing_keys.json"
)
TEST_INGREDIENTS_INVALID_VALUE_TYPE_1_JSON : str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_invalid_value_type_1.json"
)
TEST_INGREDIENTS_INVALID_VALUE_TYPE_2_JSON : str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_invalid_value_type_2.json"
)
TEST_INGREDIENTS_INVALID_VALUE_TYPE_3_JSON : str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_invalid_value_type_3.json"
)
TEST_INGREDIENTS_INVALID_VALUE_TYPE_4_JSON : str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_invalid_value_type_4.json"
)
TEST_INGREDIENTS_INVALID_VALUE_TYPE_5_JSON : str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_invalid_value_type_5.json"
)
TEST_INGREDIENTS_INVALID_VALUE_TYPE_6_JSON : str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_invalid_value_type_6.json"
)
TEST_INGREDIENTS_INVALID_VALUE_TYPE_7_JSON : str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_invalid_value_type_7.json"
)
TEST_INGREDIENTS_INVALID_VALUE_TYPE_8_JSON : str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_invalid_value_type_8.json"
)
TEST_INGREDIENTS_INVALID_VALUE_TYPE_9_JSON : str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients_invalid_value_type_9.json"
)

# Paths to the test effects data files
TEST_EFFECTS_JSON : str = path.join(
    path.dirname(__file__), "assets/test_sample_effects.json"
)

# grab module we are testing
import pytest
import util

"""

Testing the function get_ingredient_adjacency_lists

"""

def test_get_ingredient_adjacency_lists_basic() :

    pass

def test_get_ingredient_adjacency_lists_small() :
    """ Ensure that the function works with a JSON input where the ingredient has no replaces_on_mix """
    adj_lists = util.get_ingredient_adjacency_lists(TEST_INGREDIENTS_SMALL_JSON)

    # Check the adjacency list for the ingredient
    assert adj_lists['0'] == [
        ('test_ingredient_0', 0)
    ]
    pass

# def test_get_ingredient_adjacency_lists_typing() :
#     pass

# def test_get_ingredient_adjacency_lists_value_error_1() :
#     pass

# def test_get_ingredient_adjacency_lists_value_error_2() :
#     pass

# def test_get_ingredient_adjacency_lists_value_error_3() :
#     pass

# def test_get_ingredient_adjacency_lists_value_error_4() :
#     pass

# def test_get_ingredient_adjacency_lists_value_error_5() :
#     pass

# def test_get_ingredient_adjacency_lists_value_error_6() :
#     pass

# def test_get_ingredient_adjacency_lists_value_error_7() :
#     pass

# def test_get_ingredient_adjacency_lists_value_error_8() :
#     pass

# def test_get_ingredient_adjacency_lists_value_error_9() :
#     pass

def test_get_ingredient_adjacency_lists_missing_key_error() :
    """ Ensure that a MissingKeyError is raised when a required key is missing in the JSON file """
    with pytest.raises(util.MissingKeyError) as e :
        util.get_ingredient_adjacency_lists(TEST_INGREDIENTS_MISSING_KEY)

    # Check the message raised exception
    assert (
        str(e.value) == "Missing required keys in ingredient 3: {'effect_given', 'name'}" or 
        str(e.value) == "Missing required keys in ingredient 3: {'name', 'effect_given'}"
    )
    pass

def test_get_ingredient_adjacency_lists_file_not_found_error() :
    """ Ensure that a FileNotFoundError is raised when the file does not exist """
    with pytest.raises(FileNotFoundError) as e :
        util.get_ingredient_adjacency_lists(TEST_INGREDIENTS_FILE_NOT_FOUND_POINTER)
    
    # Check the message raised exception
    assert str(e.value) == f"File not found: {TEST_INGREDIENTS_FILE_NOT_FOUND_POINTER}"
    pass

def test_get_ingredient_adjacency_lists_file_incorrect_extension() :
    """ Ensure that an InvalidFileExtentionError is raised when the file does not have a .json extension """
    with pytest.raises(util.InvalidFileExtentionError) as e:
        util.get_ingredient_adjacency_lists(TEST_INGREDIENTS_INVALID_FILE_EXTENSION)
    
    # Check the message raised exception
    assert str(e.value) == "The file must have a .json extension."
    pass

"""

Testing the function get_effect_details

"""

pass