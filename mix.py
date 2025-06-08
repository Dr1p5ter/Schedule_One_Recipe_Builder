import util

from numpy import uint16, float32, array, where, append, round
from numpy.typing import NDArray
from typing import Dict, List, Tuple, Union

MAX_INGREDIENTS : uint16 = uint16(8)

class Mix:
    def __init__(self, ingredients_file_path: str, effects_file_path: str):
        """
        __init__ (dunder method)

        Initializes a Mix object with the given file paths for ingredients and effects.
        This method sets up the initial state of the mix, including empty arrays for effects and order of ingredients.
        It also loads the ingredient adjacency lists and effect details from the specified files.

        Parameters
        ----------
        ingredients_file_path : str
            Path to the ingredients file containing adjacency lists.
        effects_file_path : str
            Path to the effects file containing effect details.
        """
        self._ingredients_file_path : str = ingredients_file_path
        self._effects_file_path : str = effects_file_path
        self.mix_effects: NDArray[uint16] = array([], dtype=uint16)
        self.mix_order: NDArray[uint16] = array([], dtype=uint16)

    def __str__(self) -> str:
        """
        __str__ (dunder method)

        Returns a string representation of the Mix object, including the effects and order of ingredients.

        Returns
        -------
        str
            String representation of the Mix object.
        """
        return (
            f"Mix(effects={self.mix_effects.tolist()}, "
            f"order={self.mix_order.tolist()})"
        )

    def add_ingredient(self, ingredient: uint16):
        # Load the ingredient adjacency lists
        try:
            ingredient_adjacency_lists = util.get_ingredient_adjacency_lists(self._ingredients_file_path)
        except FileNotFoundError as e:
            raise FileNotFoundError("Ingredient adjacency lists file not found.") from e
        except ValueError as e:
            raise ValueError("Error parsing ingredient adjacency lists file.") from e
        except util.InvalidFileExtentionError as e:
            raise util.InvalidFileExtentionError("Invalid file extension for ingredient adjacency lists file.") from e
        except util.MissingKeyError as e:
            raise util.MissingKeyError("Missing required key in ingredient adjacency lists file.") from e

        # Make sure the ingredient actually exists first
        if str(ingredient) not in ingredient_adjacency_lists.keys():
            raise InvalidIngredientException(ingredient)
        
        # Make sure the number of mixes isn't already at max ingredients
        if self.mix_order.size == MAX_INGREDIENTS:
            raise MaximumIngredientsAddedException()
        
        # Make sure the last ingredient added isn't the one being added again
        if self.mix_order.size > 0:
            if self.mix_order[-1] == ingredient:
                raise DuplicateIngredientException(ingredient)
        
        # Go through effects and begin replacement
        for effect in ingredient_adjacency_lists[str(ingredient)][1:]:
            self.mix_effects = where(self.mix_effects == effect[0], effect[1], self.mix_effects)

        # Add the ingredient effect as a new effect
        self.mix_effects = append(self.mix_effects, ingredient_adjacency_lists[str(ingredient)][0][1])

        # Add ingredient as last ingredient added and put it in mix order
        self.mix_order = append(self.mix_order, ingredient)

    def get_multiplier(self) -> float32:
        # Load the effect details
        try:
            effect_details = util.get_effect_details(self._effects_file_path)
        except FileNotFoundError as e:
            raise FileNotFoundError("Effect details file not found.") from e
        except ValueError as e:
            raise ValueError("Error parsing effect details file.") from e
        except util.InvalidFileExtentionError as e:
            raise util.InvalidFileExtentionError("Invalid file extension for effect details file.") from e
        except util.MissingKeyError as e:
            raise util.MissingKeyError("Missing required key in effect details file.") from e

        # Calculate the multiplier based on the effects, rounding at each step
        multiplier = 0.0
        for effect in self.mix_effects:
            # Check if the effect is valid
            if str(effect) not in effect_details.keys():
                raise InvalidEffectException(effect)

            # add the mult value to the multiplie
            multiplier += float(effect_details[str(effect)]['value'])
        return float32(round(multiplier, 2))

class MixException(Exception):
    """Base class for all mix exceptions."""
    pass

class InvalidIngredientException(MixException):
    """Raised when an invalid ingredient is added to the mix."""
    def __init__(self, ingredient: uint16, message: str = "Invalid ingredient added to mix."):
        self.ingredient = ingredient
        self.message = f'{message} Invalid Ingredient: {ingredient}'
        super().__init__(self.message)

class InvalidEffectException(MixException):
    """Raised when an invalid effect is encountered in the mix."""
    def __init__(self, effect: uint16, message: str = "Invalid effect encountered in mix."):
        self.effect = effect
        self.message = f'{message} Invalid Effect: {effect}'
        super().__init__(self.message)

class MaximumIngredientsAddedException(MixException):
    """Raised when the maximum number of ingredients (8) is added to the mix."""
    def __init__(self, message: str = "Maximum number of ingredients added to mix."):
        self.message = message
        super().__init__(self.message)

class DuplicateIngredientException(MixException):
    """Raised when the same ingredient is added to the mix twice in a row."""
    def __init__(self, ingredient: uint16, message: str = "Duplicate ingredient added to mix."):
        self.ingredient = ingredient
        self.message = f'{message} Duplicate Ingredient: {ingredient}'
        super().__init__(self.message)
