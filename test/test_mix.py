# Ensure scope of test includes parent directory
from numpy import uint16, float32, issubdtype
from os import path
from pytest import raises
from sys import path as syspath

# Add parent directory to sys.path so we can import util
syspath.insert(0, path.abspath(path.join(path.dirname(__file__), '..')))

# Paths to the test data files
TEST_INGREDIENTS_JSON: str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredients.json"
)
TEST_INGREDIENT_INVALID_EFFECT_CORRELATION_JSON: str = path.join(
    path.dirname(__file__), "assets/test_sample_ingredient_invalid_effect_correlation.json"
)
TEST_EFFECTS_JSON: str = path.join(
    path.dirname(__file__), "assets/test_sample_effects.json"
)

# Import the util module from the parent directory
import mix

def test_mix_init():
    """Test the initialization of the Mix class."""
    mix_instance = mix.Mix(TEST_INGREDIENTS_JSON, TEST_EFFECTS_JSON)
    
    # Check if mix_effects and mix_order are initialized correctly
    assert mix_instance._ingredients_file_path == TEST_INGREDIENTS_JSON
    assert mix_instance._effects_file_path == TEST_EFFECTS_JSON
    assert issubdtype(mix_instance.mix_effects.dtype, uint16)
    assert issubdtype(mix_instance.mix_order.dtype, uint16)
    assert mix_instance.mix_effects.size == 0
    assert mix_instance.mix_order.size == 0

    pass

def test_mix_add_ingredient():
    """Test adding a valid ingredient to the mix."""
    mix_instance = mix.Mix(TEST_INGREDIENTS_JSON, TEST_EFFECTS_JSON)
    
    # Add a valid ingredient
    mix_instance.add_ingredient(uint16(0))
    
    # Check if the ingredient was added correctly
    assert mix_instance.mix_order[-1] == uint16(0)
    assert mix_instance.mix_effects.size == 1  # Assuming the effect for ingredient 0 is valid

    pass

def test_mix_add_upgrade_ingredient():
    """Test adding an upgrade ingredient to the mix."""
    mix_instance = mix.Mix(TEST_INGREDIENTS_JSON, TEST_EFFECTS_JSON)
    
    # Add valid ingredients
    mix_instance.add_ingredient(uint16(0)) # effects are [0]
    mix_instance.add_ingredient(uint16(7))  # effects are [4,7]
    mix_instance.add_ingredient(uint16(8))  # effects are [2,7,8]
    
    # Check if the effects are updated correctly
    assert mix_instance.mix_effects.size == 3  # Assuming the effects for ingredients 0, 7, and 8 are valid

    # Check if the last ingredient added is 8
    assert mix_instance.mix_order[-1] == uint16(8)

    # Check if the effects are as expected
    assert mix_instance.mix_effects.tolist() == [2, 7, 8]  # Assuming these are the expected effects

    pass

def test_mix_add_invalid_ingredient():
    """Test adding an invalid ingredient to the mix."""
    mix_instance = mix.Mix(TEST_INGREDIENTS_JSON, TEST_EFFECTS_JSON)

    # Add an invalid ingredient
    with raises(mix.InvalidIngredientException):
        mix_instance.add_ingredient(uint16(999))  # Assuming 999 is invalid

    pass
    
def test_mix_add_duplicate_ingredient():
    """Test adding a duplicate ingredient to the mix."""
    mix_instance = mix.Mix(TEST_INGREDIENTS_JSON, TEST_EFFECTS_JSON)
    
    # Add a valid ingredient
    mix_instance.add_ingredient(uint16(0))
    
    # Try to add the same ingredient again
    with raises(mix.DuplicateIngredientException):
        mix_instance.add_ingredient(uint16(0))

    pass

def test_mix_add_max_ingredients():
    """Test adding ingredients until the maximum is reached."""
    mix_instance = mix.Mix(TEST_INGREDIENTS_JSON, TEST_EFFECTS_JSON)
    
    # Add maximum number of ingredients
    for i in range(mix.MAX_INGREDIENTS):
        mix_instance.add_ingredient(uint16(i))
    
    # Check if the last ingredient added is the maximum
    assert mix_instance.mix_order[-1] == uint16(mix.MAX_INGREDIENTS - 1)
    
    # Try to add one more ingredient
    with raises(mix.MaximumIngredientsAddedException):
        mix_instance.add_ingredient(uint16(mix.MAX_INGREDIENTS))

    pass

def test_mix_get_multiplier():
    """Test getting the multiplier from the mix."""
    mix_instance = mix.Mix(TEST_INGREDIENTS_JSON, TEST_EFFECTS_JSON)
    
    # Add a valid ingredient
    mix_instance.add_ingredient(uint16(0))
    
    # Get the multiplier
    multiplier = mix_instance.get_multiplier()
    
    # Check if the multiplier is a float
    assert issubdtype(multiplier.dtype, float32)
    assert multiplier == float32(0.12)  # Assuming the effect for ingredient 0 gives a multiplier of 0.12

    pass

def test_mix_get_multiplier_invalid_effect():
    """Test getting the multiplier with an invalid effect."""
    mix_instance = mix.Mix(TEST_INGREDIENT_INVALID_EFFECT_CORRELATION_JSON, TEST_EFFECTS_JSON)
    
    # Add an ingredient that has an invalid effect
    mix_instance.add_ingredient(uint16(0))
    
    # Try to get the multiplier
    with raises(mix.InvalidEffectException):
        mix_instance.get_multiplier()

    pass
