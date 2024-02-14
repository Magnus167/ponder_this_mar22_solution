from typing import List, Union, Any, Generator, Dict, Tuple, overload

import numpy as np
import random
from functools import lru_cache

SRandInt = random.SystemRandom().randint

# from .solve.primes import is_prime, get_primes, generate_primes

DICES_FACES = [
    (1, 4),
    (1, 6),
    (1, 8),
    (0, 9),
    (1, 12),
    (1, 20),
]

DICES = [list(range(faces[0], faces[1] + 1)) for faces in DICES_FACES]


@overload
def expand_dice_tuple(dice: List[Tuple[int, int]]) -> List[List[int]]: ...


def expand_dice_tuple(dice: Tuple[int, int]) -> List[int]:
    if isinstance(dice, tuple):
        return list(map(expand_dice_tuple, dice))
    return list(range(dice[0], dice[1] + 1))


def _get_combinations(dices: List[List[int]]) -> Generator[List[int], None, None]:
    if not dices:
        return
    if len(dices) == 1:
        for dice in dices[0]:
            yield [dice]
        return
    for dice in dices[0]:
        for combination in _get_combinations(dices[1:]):
            yield [dice] + combination


@lru_cache(maxsize=None)
def _get_combos_cache(dices_str: str) -> List[List[int]]:
    dices = eval(dices_str)
    return list(_get_combinations(dices))


# get all possible combinations of dices
def get_combinations(dice_faces: List[Tuple[int, int]]) -> List[List[int]]:
    dices = [list(range(faces[0], faces[1] + 1)) for faces in dice_faces]
    # return list(_get_combinations(dices_str))
    dices_str = str(dices)
    return _get_combos_cache(dices_str)


def throw(dices: List[Tuple[int, int]]) -> int:
    return [random.randint(dice[0], dice[1]) for dice in dices]


def throw_sum(dices: List[Tuple[int, int]]) -> int:
    return sum(throw(dices))


def get_unique_throw_sums(dices: List[Tuple[int, int]]) -> List[int]:
    return list(set(map(sum, get_combinations(dices))))


def get_unique_throw_sums_dict(dices: List[Tuple[int, int]]) -> Dict[int, int]:
    result = {}
    for gc in get_combinations(dices):
        s = sum(gc)
        result[s] = result.get(s, 0) + 1

    return result


get_unique_throw_sums(DICES_FACES)

get_unique_throw_sums_dict(DICES_FACES)
