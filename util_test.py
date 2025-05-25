import os
import pytest
from numpy import uint16, float32, isclose, issubdtype
from util import get_ingredient_adjacency_lists, get_effect_details

# util_test.py
# Automated tests for util.py using pytest.
# These tests check the correctness of get_ingredient_adjacency_lists and get_effect_details
# using the provided effects.json and ingredients.json files.
# No external sources used; see https://docs.pytest.org/en/stable/ for pytest usage.

# Paths to the test data files (assumes tests run from project root)
INGREDIENTS_JSON = os.path.join(os.path.dirname(__file__), "ingredients.json")
EFFECTS_JSON = os.path.join(os.path.dirname(__file__), "effects.json")


def test_get_ingredient_adjacency_lists_basic():
    """Test that the adjacency list is parsed correctly for a known ingredient."""
    adj = get_ingredient_adjacency_lists(INGREDIENTS_JSON)

    # Check that all expected ingredient keys are present
    assert "0" in adj
    assert "1" in adj
    assert "15" in adj

    # Check the structure for ingredient "0" (addy)
    addy = adj["0"]
    assert isinstance(addy, list)

    # First tuple: (name, effect_given)
    assert addy[0][0] == "addy"
    assert addy[0][1] == uint16(30)

    # Check that replaces_on_mix entries are correct
    expected_replaces = [
        (uint16(11), uint16(10)),
        (uint16(13), uint16(9)),
        (uint16(15), uint16(21)),
        (uint16(18), uint16(8)),
        (uint16(23), uint16(14)),
    ]
    assert addy[1:] == expected_replaces


def test_get_ingredient_adjacency_lists_types():
    """Test that all keys and values in the adjacency list have the correct types."""
    adj = get_ingredient_adjacency_lists(INGREDIENTS_JSON)
    for ing_id, tuples in adj.items():
        assert isinstance(ing_id, str)
        assert isinstance(tuples, list)

        # First tuple: (str, uint16)
        assert isinstance(tuples[0][0], str)
        assert issubdtype(type(tuples[0][1]), uint16)

        # Rest: (uint16, uint16)
        for t in tuples[1:]:
            assert issubdtype(type(t[0]), uint16)
            assert issubdtype(type(t[1]), uint16)


def test_get_ingredient_adjacency_lists_full_coverage():
    """Test that all ingredients and their replaces_on_mix are parsed correctly."""
    adj = get_ingredient_adjacency_lists(INGREDIENTS_JSON)

    # Check a more complex ingredient
    banana = adj["1"]
    assert banana[0][0] == "banana"
    assert banana[0][1] == uint16(14)

    # Check specific replaces_on_mix mappings
    assert (uint16(4), uint16(28)) in banana
    assert (uint16(31), uint16(27)) in banana


def test_get_effect_details_basic():
    """Test that effect details are parsed correctly for a known effect."""
    effects = get_effect_details(EFFECTS_JSON)
    assert "0" in effects
    assert "30" in effects

    # Check anti_gravity
    anti_gravity = effects["0"]
    assert anti_gravity["name"] == "anti_gravity"
    assert isclose(anti_gravity["value"], float32(0.54))

    # Check thought_provoking
    tp = effects["30"]
    assert tp["name"] == "thought_provoking"
    assert isclose(tp["value"], float32(0.44))


def test_get_effect_details_types():
    """Test that all effect details have the correct types."""
    effects = get_effect_details(EFFECTS_JSON)
    for effect_id, details in effects.items():
        assert isinstance(effect_id, str)
        assert isinstance(details, dict)
        assert isinstance(details["name"], str)
        assert issubdtype(type(details["value"]), float32)


def test_get_effect_details_full_coverage():
    """Test that all effects from the JSON are present and correct."""
    effects = get_effect_details(EFFECTS_JSON)

    # There should be 34 effects (0-33)
    assert len(effects) == 34

    # Check a zero-value effect
    assert effects["7"]["name"] == "disorienting"
    assert isclose(effects["7"]["value"], 0.0)

    # Check a high-value effect
    assert effects["25"]["name"] == "shrinking"
    assert isclose(effects["25"]["value"], 0.60)


def test_get_ingredient_adjacency_lists_and_effect_details_integration():
    """
    Integration test: ensure that effect_given and replaces_on_mix values
    match effect ids in effects.json.
    """
    adj = get_ingredient_adjacency_lists(INGREDIENTS_JSON)
    effects = get_effect_details(EFFECTS_JSON)
    for ing_id, tuples in adj.items():
        # Check effect_given exists in effects
        effect_given = str(tuples[0][1])
        assert (
            effect_given in effects
            or int(effect_given) in [int(k) for k in effects.keys()]
        )

        # Check all replaces_on_mix keys/values exist in effects
        for t in tuples[1:]:
            assert str(t[0]) in effects
            assert str(t[1]) in effects


if __name__ == "__main__":
    pytest.main([__file__])