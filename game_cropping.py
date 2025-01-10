from typing import Any
import numpy as np


def get_game_height_ratio(cropped_game: np.ndarray[Any, np.dtype[np.integer[Any] | np.floating[Any]]]) -> float:
    # Crop the game area
    original_game_height, original_game_width = (885, 674)
    game_height, game_width = cropped_game.shape[0:2]
    game_height_ratio = game_height / original_game_height

    return game_height_ratio

def get_img_slice(
    image: np.ndarray[Any, np.dtype[np.integer[Any] | np.floating[Any]]],
    h: int,
    slice_number: int = 0,
    ratio: float = 1.0,
    my_min: int = 180,
    my_max: int = 280
) -> np.ndarray[Any, np.dtype[np.integer[Any] | np.floating[Any]]]:
    my_min *= ratio
    my_max *= ratio

    offset = slice_number * 100 * ratio

    return image[int(h - (my_max + offset)): int(h - (my_min + offset))]
